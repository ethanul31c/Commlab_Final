function sig_CFO_corrected = CFO_correction(sig, L, cfo_ppm)
    global ts;
    global fc;
    global fs;

    delta_f= fc*cfo_ppm/1e6;
    
    t = (0:L-1) * ts;
    idx = exp(-1j*2*pi* delta_f .*t);
    sig_CFO_corrected = sig .* idx(:);
end