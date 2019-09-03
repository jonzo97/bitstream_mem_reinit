module ramb4k8 #(parameter DWID = 8, AWID = 12) (input logic[AWID-1:0] addr, input logic[DWID-1:0]  din, output logic[DWID-1:0] dout, input logic wen, input logic clk);
  (* ram_style = "block" *) logic[DWID-1:0] mem[1<<AWID];

   
   always @(posedge clk)
     begin
        if (wen) 
          mem[addr] <= din;
        dout <= mem[addr];
     end

   initial begin
      mem[0] = 8'hF0;
   end
   

endmodule // rambA

     
