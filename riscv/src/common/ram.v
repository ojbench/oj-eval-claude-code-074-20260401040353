// Simple RAM module
module ram #(
    parameter SIZE = 131072  // 128KB
) (
    input wire clk,
    input wire rst,
    input wire rdy,

    input  wire [31:0] addr,
    input  wire [7:0]  data_in,
    output reg  [7:0]  data_out,
    input  wire        wr
);

    reg [7:0] memory [0:SIZE-1];

    always @(posedge clk) begin
        if (rst) begin
            data_out <= 8'h0;
        end else if (rdy) begin
            if (wr) begin
                if (addr < SIZE) begin
                    memory[addr] <= data_in;
                end
            end else begin
                if (addr < SIZE) begin
                    data_out <= memory[addr];
                end else begin
                    data_out <= 8'h0;
                end
            end
        end
    end

endmodule
