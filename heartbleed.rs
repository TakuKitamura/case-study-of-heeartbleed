
// fn parse(
//     ptr_request: &[u8],
//     request_size: usize,
//     mut ptr_payload_length: u32,
//     ptr_error_code: &u8
//  ) {
//     //  let a = request_size - 2;
//      let mut response: Vec<u8> = Vec::with_capacity(request_size - 2);
//     // let temp: u32 = ((ptr_request[0] as u32) << 8 | (ptr_request[1] as u32));
//     ptr_payload_length = ((ptr_request[0] as u32) << 8 | (ptr_request[1] as u32));
//     response.extend(ptr_request)
// }

fn main() {
    let request = vec![0x00, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64];
    let request_size: usize = request.len();
    if request_size < 3 ||  request_size > 65535 + 2 {
        println!("request_size is invalid.\nrequest_size = {}\n", request_size);
        std::process::exit(1);
    }

    let mut response: Vec<u8> = Vec::with_capacity(request_size - 2);
    let payload_length: u32 = (request[0] as u32) << 8 | (request[1] as u32);
    response.extend(request[2..2+payload_length as usize].iter().cloned());

    for i in 0..payload_length {
        print!("{}", response[i as usize] as char);
    }
    std::process::exit(0);
 }