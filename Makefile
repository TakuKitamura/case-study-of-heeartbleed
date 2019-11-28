fstar:
	krml -verify -drop WasmSupport -tmpdir ./out -fsopt --cache_dir -fsopt ./out -no-prefix Heartbleed -o ./out/fstar_heartbleed.out heartbleed.fst memcpy.c fstar_heartbleed.c && ./out/fstar_heartbleed.out
c:
	gcc c_heartbleed.c -o ./out/c_heartbleed.out
rust:
	rustc rust_heartbleed.rs -o ./out/rust_heartbleed.out