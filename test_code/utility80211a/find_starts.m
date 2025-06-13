% find starts
function [sts_start, frame_starts, ofdm_start] = find_starts(buffer_trimmed, sec_beg, single_LTS, N, sym_num)
    conv_sig_LTS = conv(buffer_trimmed, flipud(conj(single_LTS)), "valid"); % index range should be adjusted
    plot(abs(conv_sig_LTS));
    saveas(gcf, "conv.png")
    % pause(10)
    frame_starts = zeros(1,N);
    for ii = 1:N
        conv_sig_LTS = conv(buffer_trimmed, flipud(conj(single_LTS)), "valid"); % index range should be adjusted
        crit_lts = max(abs(conv_sig_LTS))*0.7;
        lts_peaks = find(abs(conv_sig_LTS) >= crit_lts);
        frame_starts(ii) = lts_peaks(1);
        buffer_trimmed(frame_starts(ii) - 160 - 32: ...
                       frame_starts(ii) + 160 + sym_num * 64) = 0;
    end

    % lts_peaks = find(abs(conv_sig_LTS) >= crit_lts);
    % if(length(lts_peaks)) == 2*N
    %     idx = (1:length(lts_peaks)/2);
    %     frame_starts = lts_peaks(idx.*2-1);
    % elseif(length(lts_peaks)) == 4*N
    %     idx = (1:length(lts_peaks)/4);
    %     frame_starts = lts_peaks(idx.*4-3);
    % end
    fprintf("length of lts_peak = %d\n",length(lts_peaks))
    %lts_start = sec_beg + lts_peaks(1)-1;

    sts_start = sec_beg + lts_peaks(1)-1 - 32 - 160;
    ofdm_start = sts_start + 360;
end

