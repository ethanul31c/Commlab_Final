function plot_buffer()
    global ts;
    buffer = 0; % 占掉名稱

    load("received_test.mat");

    figure;
    
    time_vector = (1:length(buffer));
    plot(time_vector, real(buffer), 'Color', '#003C76');
    hold on
    xline(sts_start, 'Color', '#393939','LineWidth', 1);

    for i = 1:length(frame_starts)
        xline(frame_starts(i), 'Color', '#939880','LineWidth', 1);
    end
    % xline(frame_starts, 'Color', '#939880','LineWidth', 1);
    xline(ofdm_start, 'Color', '#875B75','LineWidth', 1);
    % xline(sts_start + length(sig), 'Color', '#DAC1AE','LineWidth', 1);
    hold off
    %xlim([sec_beg sec_end]);
    xt = xticks;
    xticklabels(xt * ts*1e6);
    xlabel('Time (microseconds)');
    ylabel('Amplitude');
    title('Time-Domain received signal (real)');
    legend('received signal','sts\_start', 'lts\_start', 'ofdm\_start', 'frame\_end');
end

plot_buffer();
