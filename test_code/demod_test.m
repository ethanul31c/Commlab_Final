function SNR_dB = demod_test(ENABLE_PROTOCOL, filename, QAM_size_int)
    % clc; clear; close all;
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
    
    % color style
    % '#003C76': Deep Blue
    % '#939880': Tea Green
    % '#875B75': Plum Purple
    % '#DAC1AE': Skin Pink
    % '#99755A': Brown
    % '#393939': Black
    
    %% load function kits and bitstream
    % filename = "Peppers_bit";
    addpath('utility80211a\');
    file_str = sprintf("%s.mat", filename);
    load(file_str);
    
    %% generate sections
    
    
    % K-OFDM
    NUM_SYMBOLS_IN_A_FRAME = 100;  % number of ofdm symbols in each frame
    L_head  = 320;
    L_sig   = L_head + NUM_SYMBOLS_IN_A_FRAME * (N_OFDM);
    % scaling of transmitted amplitude
    % send_amp = 0.1;
    
    % segmenting bitstream
    
    % QAM_size = 64; % 4 for 4 QAM
	QAM_size = double(QAM_size_int);
    NUM_BITS_PER_SYMBOL = log2(QAM_size) * length(data_idx); % 96 for 4QAM
    
    
    LEN_SEC = NUM_BITS_PER_SYMBOL * NUM_SYMBOLS_IN_A_FRAME; % bits/frame, 9600 default 
    pad_len = mod(-length(bits_tx), LEN_SEC);  % 算出還差幾個補到 M 的倍數
    bits_tx_padded = [bits_tx, zeros(1, pad_len)];  % 補 0
    bits_tx_matrix = reshape(bits_tx_padded, LEN_SEC, []).';  % 每 row 有 LEN_SEC 個
    [NUM_OF_SIG_FRAME, ~] = size(bits_tx_matrix);

    
    
    buffer = 0; % 占掉名稱
    %load ("received_test.mat")
    savename = sprintf("%s_channel_%dQAM.mat",filename, QAM_size_int);
    load (savename);
    % plot_whole_buffer();
    
    bits_rx = zeros('logical');
    SNR = 0;
    
    for i = 1: NUM_OF_SIG_FRAME
        %% P_sig (for SNR calculation)
        ofdm_start = frame_starts(i) + 128 +;
        P_sig = mean(abs(buffer(ofdm_start:ofdm_start+NUM_SYMBOLS_IN_A_FRAME*(N_FFT+N_CP)-1)).^2);
        P_noise = mean(abs([ ...
            buffer((frame_starts(i)-128-100):(frame_starts(i)-128-1));...
            buffer((ofdm_start+NUM_SYMBOLS_IN_A_FRAME*(N_FFT+N_CP)):...
            (ofdm_start+NUM_SYMBOLS_IN_A_FRAME*(N_FFT+N_CP)+100))]).^2);
        SNR = SNR + P_sig/P_noise;


        %% CFO correction
        symbol_start= frame_starts(i) + 128;
        lts_start_1 = frame_starts(i);
        lts_start_2 = frame_starts(i) + 64;
        sig_beg = lts_start_1-32-160;
        sig_end = sig_beg + L_sig - 1;
    
        lts_1 = buffer(lts_start_1:lts_start_1 + 64-1);
        lts_2 = buffer(lts_start_2:lts_start_2 + 64-1);
        % plot(real(buffer(lts_start_1:lts_start_2 + 64-1)))
        phase_diff = angle(sum(lts_2 .* conj(lts_1)));
        cfo_hz = phase_diff / (2*pi*64*ts);  % 64 is time diff between 8th and 10th
        cfo_ppm = cfo_hz / fc * 1e6;
        
        % fprintf("CFO estimated by consecutive LTS(PPM) = %.2f", cfo_ppm);
    
    
        sig_CFO_corrected = CFO_correction(buffer(sig_beg:sig_end), sig_end-sig_beg+1, cfo_ppm);
    
        %% channel estimation
        H1 = channel_est_LTS(sig_CFO_corrected, lts_start_1-sig_beg+1);
        H2 = channel_est_LTS(sig_CFO_corrected, lts_start_1-sig_beg+1+64);
    
        H_est = (H1+H2)/2;
        Data_rx = zeros(length(data_idx)*NUM_SYMBOLS_IN_A_FRAME, 1);
        Pilot_rx = zeros(length(pilot_idx)*NUM_SYMBOLS_IN_A_FRAME, 1);
        
        %% Equalization and residue CFO Correction
    
        for ii = 0:NUM_SYMBOLS_IN_A_FRAME-1 %!!!!!P_OFDM to be determined
            sig_c = ofdm_removeCP(sig_CFO_corrected(L_head+1 + ii*(N_FFT+N_CP): L_head + (ii+1)*(N_FFT+N_CP)));
            X_rx = fftshift(fft(sig_c));
            [Pilot, Data] = Equalize(X_rx, H_est); % H_est = (H1+H2)/2;
    
            Q = [1; 1; 1; 1];
            res_CFO_phase = Res_CFO_calc(Pilot, Q);
            Data_res_CFO_corrected = Res_CFO_correction(Data, res_CFO_phase);
            Data_rx(48*ii+1 : 48*(ii+1)) = Data_res_CFO_corrected;
            Pilot_rx(4*ii+1 : 4*(ii+1)) = Pilot;
        end
        
        Data_rx = Data_rx / sqrt(mean(abs(Data_rx).^2));
        % for i = 0:(NUM_OF_SIG_FRAME-1)
        %     for j = 0:(NUM_SYMBOLS_IN_A_FRAME-1)
        %         bit_groups  = reshape(bits_tx(i*), log2(mod_size), []).';
        %         sym_indices = bi2de(bit_groups, 'left-msb');  % MSB first
        %         qam_mod     = qammod(sym_indices, mod_size, 'UnitAveragePower', true);
        % 
        %     end
        % end

        Pilot_rx = Pilot_rx / sqrt(mean(abs(Pilot_rx).^2));

        if i == NUM_OF_SIG_FRAME-1
            
            I_data = real(Data_rx);
            Q_data = imag(Data_rx);
            I_pilot = real(Pilot_rx);
            Q_pilot = imag(Pilot_rx);
    
            % ideal symbols
            ideal_symbols = qammod(0:QAM_size-1, QAM_size, 'gray', 'UnitAveragePower', true);
            Ii = real(ideal_symbols);
            Qi = imag(ideal_symbols);
    
            % plot data and pilot
            close all;
            figure(1);
            plot(I_pilot, Q_pilot, 'o','Color', '#939880', 'MarkerFaceColor', 'r', 'MarkerSize', 1); 
            hold on;
            plot(I_data, Q_data, 'o', 'Color', '#875B75', 'MarkerFaceColor', 'r', 'MarkerSize', 1); 
    
            % plot ideal symbol
            plot(Ii, Qi, 'x', 'Color', '#003C76', 'MarkerSize', 5, 'LineWidth', 1);
            I_bpsk = [1, -1];
            Q_bpsk = [0, 0];
            plot(I_bpsk, Q_bpsk, 'bx', 'MarkerSize', 5, 'LineWidth', 2); 
    
    
            axis([-1.5 1.5 -1.5 1.5]);
            xlabel('I(t)');
            ylabel('Q(t)');
    
            xline(0, 'k', 'LineWidth', 1); % Real axis (vertical)
            yline(0, 'k', 'LineWidth', 1); % Imaginary axis (horizontal)
            legend({'received pilots', 'received data', 'ideal modulation'}, 'Location', 'northeast');
            title('8. Received Constellation with CFO corrected');
    
            axis equal;
            grid on;
            hold off;
        end
    
        %% demodulation
    
        data_rx_bits = qamdemod(Data_rx, QAM_size, 'gray', 'UnitAveragePower', true, OutputType="bit");
        bits_rx(1+(i-1)*length(data_rx_bits) : i*length(data_rx_bits)) = data_rx_bits;
    end
    
    SNR = SNR / NUM_OF_SIG_FRAME;
    SNR_dB = 10*log(SNR);
    
    numErrors = sum(bits_tx~=bits_rx(1:length(bits_tx)));
    BER = (numErrors/length(bits_rx));
    
    file_str = sprintf("%s_received.mat", filename);
    save(file_str, "bits_rx")
    fprintf("SNR = %.5f dB\n", SNR_dB);
    fprintf("BER = %.5f\n", BER);
    
end

%demod_tes()
