module top(
input logic clk,
input logic[31:0] raddr,
input logic[31:0] waddr,
input logic [0:0] din,
output logic [0:0] dout,
input logic reset);

memory #("~/bigmems/designs/init/1_by_16k.txt", 1, 1, 16384) mem(
	.clk(clk), 
	.raddr(raddr), 
	.waddr(waddr), 
	.din(din), 
	.dout(dout), 
	.reset(reset));


endmodule