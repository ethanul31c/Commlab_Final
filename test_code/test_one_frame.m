function received_buffer = test_one_frame()
    
    clc; clear; close all;
    
    addpath('utility80211a\');
    
    global pilot_idx;
    global data_idx;
    global zero_idx;
    global channel_est
    global N_FFT;
    global N_CP;
    global N_OFDM;
    global fs;
    global ts;
    global fc;
    %% Parameters for wifi 802.11(a/g)
    N_FFT = 64;  % FFT size
    N_CP = 16;   % Cyclic prefix length
    N_OFDM = N_FFT+ N_CP;
    fs = 10e6;   % Sampling rate (Hz)
    ts = 1/fs;   % Sampling time
    fc = 915e6;  % Carrier frequency (Hz)
    
    
    % Define subcarrier indices for 802.11a/g
    pilot_idx = [12 26 40 54];   % Pilot subcarriers (1-based index)
    data_idx = setdiff(1:N_FFT, [1:6, pilot_idx, N_FFT/2+1, 1:6, 60:64]); % Exclude DC, pilot, and unused guard bands
    zero_idx = [1:6, N_FFT/2+1, 60:64];
    % 5- OFDM symbols with STS, LTS;
    L_sig_5_head = 320;
    L_sig_5 =  L_sig_5_head + 5 * (N_OFDM);
    L_sig_100   = L_sig_5_head + 100 * (N_OFDM);
    
    % scaling of transmitted amplitude
    send_amp = 0.1;
    
    % color style
    % '#003C76': Deep Blue
    % '#939880': Tea Green
    % '#875B75': Plum Purple
    % '#DAC1AE': Skin Pink
    % '#99755A': Brown
    % '#393939': Black
    
    
    L_head = 320;
    L_sig_100 = L_head + 100*N_OFDM;
    
    sig_100 = zeros(L_sig_100, 1);
    data_tx = zeros(5*48, 1);
    
    % generate frame head
    [STS, single_STS] = STS_generate();
    [LTS, single_LTS] = LTS_generate();
    sig_100(1:length(STS)) = STS;
    sig_100(length(STS)+1:length(STS)+length(LTS))= LTS;
    
    % generate 100 OFDM Symbols
    for i = 0:(100-1)
        x_fft = ofdm_generate(4); % one OFDM symbol, 4-qam
        x = ifft(ifftshift(x_fft));
        x_cp = ofdm_addCP(x);
        sig_100(L_head + i*(N_OFDM)+1 : L_head+(i+1)*(N_OFDM)) = x_cp;
        
        data_tx(48*i+1 : 48*(i+1)) = x(data_idx);
    end
    sig_100(L_head+1:end) = sig_100(L_head+1:end)/mean(abs(sig_100(L_head+1:end)));
    
    bits_tx = qamdemod(data_tx, 4, 'gray', OutputType='bit', UnitAveragePower=true);
    padded_sig_100 = send_amp*[zeros(100, 1); sig_100; zeros(100, 1)];
    
    
    l = length(padded_sig_100);
    radio_Tx = USRP_init(l, '192.168.10.2', "tx");
    radio_Rx = USRP_init(l, '192.168.10.2', "rx");
    buffer = zeros(5*l, 1);
    
    % Transmit the frame we generate
    
    for ii = 1:3
        if ii == 2
            tunderrun = radio_Tx(padded_sig_100);
        else
            tunderrun = radio_Tx(complex(zeros(l, 1)));
        end
        [rcvdSignal, ~, toverflow] = step(radio_Rx);
        buffer((1+(ii-1)*l):(ii*l)) = rcvdSignal;
    end
    % Keep reception for 2 frames
    for ii = 4:5
        [rcvdSignal, ~, toverflow] = step(radio_Rx);
        buffer((1+(ii-1)*l):(ii*l)) = rcvdSignal;
    end 
    
    release(radio_Tx)
    release(radio_Rx)
    
    
    [sec_beg, sec_end] = fast_trim(buffer, 8500, 100);
    received_buffer = buffer(sec_beg:sec_end);
    

    single_LTS = LTS(end-64+1:end);
    [sts_start, lts_start, ofdm_start] = find_starts(buffer(sec_beg:sec_end), sec_beg, single_LTS)
    fprintf("ofdm_start = %d" ,ofdm_start);

    % plot the location of estimated starts
    figure;
    time_vector = (sec_beg:sec_end);
    plot(time_vector, real(buffer(sec_beg:sec_end)), 'Color', '#003C76');
    hold on
    xline(sts_start, 'Color', '#393939','LineWidth', 1);
    xline(lts_start, 'Color', '#939880','LineWidth', 1);
    xline(ofdm_start, 'Color', '#875B75','LineWidth', 1);
    xline(sts_start + L_sig_100, 'Color', '#DAC1AE','LineWidth', 1);
    hold off
    xlim([sec_beg sec_end]);
    xt = xticks;
    xticklabels(xt * ts*1e6);
    xlabel('Time (microseconds)');
    ylabel('Amplitude');
    title('4. Time-Domain received signal (real)');
    legend('received signal','sts\_start', 'lts\_start', 'ofdm\_start', 'frame\_end');

end

