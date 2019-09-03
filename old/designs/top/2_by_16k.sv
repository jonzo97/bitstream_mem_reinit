module top(
input logic clk,
input logic[31:0] raddr,
input logic[31:0] waddr,
input logic [1:0] din,
output logic [1:0] dout,
input logic reset);

memory #("~/bigmems/designs/init/2_by_16k.txt", 1, 2, 16384) mem(
	.clk(clk), 
	.raddr(raddr), 
	.waddr(waddr), 
	.din(din), 
	.dout(dout), 
	.reset(reset));


endmodule