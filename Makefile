all:
	krml -verify -drop WasmSupport -tmpdir ./out -fsopt --cache_dir -fsopt ./out -no-prefix Heartbleed -o ./out/heartbleed.out heartbleed.fst memcpy.c call_parse.c && ./out/heartbleed.out