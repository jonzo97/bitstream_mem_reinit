module top(
input logic clk,
input logic[31:0] raddr,
input logic[31:0] waddr,
input logic [2:0] din,
output logic [2:0] dout,
input logic reset);

memory #("~/bigmems/designs/init/3_by_5k.txt", 1, 3, 5000) mem(
	.clk(clk), 
	.raddr(raddr), 
	.waddr(waddr), 
	.din(din), 
	.dout(dout), 
	.reset(reset));


endmodule