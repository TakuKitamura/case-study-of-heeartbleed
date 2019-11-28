module Heartbleed

open FStar.HyperStack.ST

module S = FStar.Seq
module B = LowStar.Buffer
module M = LowStar.Modifies
module U8 = FStar.UInt8
module U32 = FStar.UInt32
module ST = FStar.HyperStack.ST
open LowStar.BufferOps
open LowStar.Printf
open FStar.Int.Cast

#reset-options "--z3rlimit 10 --initial_fuel 0 --max_fuel 0 --initial_ifuel 0 --max_ifuel 0"

assume val memcpy: #a:eqtype -> dst:B.buffer a -> src:B.buffer a -> len: U32.t -> Stack unit
  (requires fun h0 ->
    let l_src = M.loc_buffer src in
    let l_dst = M.loc_buffer dst in
    B.live h0 src /\ B.live h0 dst /\
    B.length src = U32.v len /\
    B.length dst = U32.v len /\
    M.loc_disjoint l_src l_dst)
  (ensures fun h0 _ h1 ->
    let l_src = M.loc_buffer src in
    let l_dst = M.loc_buffer dst in
    B.live h1 src /\
    B.live h1 dst /\
    M.(modifies l_dst h0 h1) /\
    S.equal (B.as_seq h1 dst) (B.as_seq h0 src))
val parse
  (ptr_request: B.buffer U8.t)
  (request_size: U32.t{U32.v request_size >= 3 && U32.v request_size <= 65535 + 2})
  (ptr_payload_length: B.buffer U32.t)
: ST (B.buffer U8.t)
    (requires fun h -> B.live h ptr_request /\
      B.live h ptr_payload_length /\
      B.length ptr_request = U32.v request_size /\
      B.length ptr_payload_length = 1 /\
      U32.v (Seq.index (B.as_seq h ptr_payload_length) 0) = 0)
    (ensures fun h1 _ h2 -> true)
let parse ptr_request request_size ptr_payload_length =
  let ptr_response: B.buffer U8.t = B.malloc HyperStack.root 0uy (U32.sub request_size 2ul) in
  let mb: U8.t = ptr_request.(0ul) in
  let lb: U8.t = ptr_request.(1ul) in
  let mb_u32: U32.t = uint8_to_uint32 mb in
  let lb_u32: U32.t = uint8_to_uint32 lb in
  let paylaod_length: U32.t =  U32.logor (U32.shift_left mb_u32 8ul) lb_u32 in
  if (U32.((request_size -^ 2ul) = paylaod_length)) then
      (
        ptr_payload_length.(0ul) <- paylaod_length;
        let ptr_request_offset: B.buffer U8.t = B.offset ptr_request 2ul in
        memcpy ptr_response ptr_request_offset paylaod_length
      );
  // else
  //   ptr_error_code.(0ul) <- 2uy;
  ptr_response