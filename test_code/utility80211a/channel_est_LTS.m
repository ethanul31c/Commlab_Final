% Channel estimation using LTS
function H_est = channel_est_LTS(buffer_trimmed, lts_start)
    LTS_val = [1,1,-1,-1,1,1,-1,1,-1,1,1,1,1,1,1,-1,-1,1,1,-1,1,-1,1,1,1,1,0,1, ...
        -1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,-1,1,1,-1,-1,1,-1,1,-1,1,1,1,1];
    lts_1       = buffer_trimmed(lts_start : lts_start+64-1);
    LTS_1_RX    = fftshift(fft(lts_1));
    H1          = zeros(64, 1);
    est_idx     = (-26+33: 26+33); % -26 to 26 except '0'
    H1(est_idx) = LTS_1_RX(est_idx).*LTS_val.';
    H_est       = H1;
end