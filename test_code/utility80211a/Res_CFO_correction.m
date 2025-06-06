function Data_res_CFO_corrected = Res_CFO_correction(Data, res_CFO_phase)
    Data_res_CFO_corrected = Data*exp(-1j*res_CFO_phase);
end