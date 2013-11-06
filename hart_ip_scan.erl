-module(hart_ip_scan).
-export([header/5, simple_body/1, request/4, parse/1, scan_udp/1]).

header(Version, Type, ID, Seq, Length) -> 
	<<Version, Type, ID, 0, Seq:16, Length:16>>.

simple_body(Timer) -> 
	<<1, Timer:32>>.

request(Version, ID, Seq, Timer) ->
	Header_size = 8,	
	Body = simple_body(Timer),
	Header = header(Version, 0, ID, Seq, Header_size + byte_size(Body)),
	<<Header/binary, Body/binary>>.

parse(HARTIP_Packet) -> 
	<<Version:8, Type:8, ID:8, Status:8, Seq:16, Length:16, Body/binary>> = HARTIP_Packet,
	[Version, Type, ID, Status, Seq, Length, Body].

scan_udp(Host) ->
	scan_udp(Host, 5094).

scan_udp(Host, Port) ->
	{ok, Socket} = gen_udp:open(0, [binary, {active, false}]),
	gen_udp:send(Socket, Host, Port, request(1, 0, 2, 30000)),
	Value = receive 
		 {udp, Socket, _, _, Bin} -> file:write_file("hartips.txt", io:format("from ~s rcvd: ~p~n", [Host, Bin]), [append]), 1
		after 
		 3000 -> 0
		end,
	gen_udp:close(Socket),
	Value.


 