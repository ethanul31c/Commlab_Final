% find starts
function [sts_start, frame_starts, ofdm_start] = find_starts(buffer_trimmed, sec_beg, single_LTS, N)
    conv_sig_LTS = conv(buffer_trimmed, flipud(conj(single_LTS)), "valid"); % index range should be adjusted
    plot(abs(conv_sig_LTS));
    crit_lts = max(abs(conv_sig_LTS))*0.7;
    
    lts_peaks = find(abs(conv_sig_LTS) >= crit_lts);
    if(length(lts_peaks)) == 2*N
        idx = (1:length(lts_peaks)/2);
        frame_starts = lts_peaks(idx.*2-1);
    elseif(length(lts_peaks)) == 4*N
        idx = (1:length(lts_peaks)/4);
        frame_starts = lts_peaks(idx.*4-3);
    end
    fprintf("length of lts_peak = %d\n",length(lts_peaks))
    %lts_start = sec_beg + lts_peaks(1)-1;

    sts_start = sec_beg + lts_peaks(1)-1 - 32 - 160;
    ofdm_start = sts_start + 360;
end

