% find starts
function [sts_start, lts_start, ofdm_start] = find_starts(buffer_trimmed, sec_beg, single_LTS)
    conv_sig_LTS = conv(buffer_trimmed, flipud(conj(single_LTS)), "valid"); % index range should be adjusted
    crit_lts = max(abs(conv_sig_LTS))-0.15;
    
    lts_peaks = find(abs(conv_sig_LTS) >= crit_lts);
    lts_start = sec_beg + lts_peaks(1)-1;
    ofdm_start = lts_start + 2*64;
    sts_start = lts_start - 32 - 160;
end