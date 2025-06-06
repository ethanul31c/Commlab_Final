% generate single OFDM symbol
function ofdm_SYM = ofdm_generate(mod_size, data_bits)
    % Generate pilot tones (BPSK modulation)
    global pilot_idx;
    global data_idx;
    global N_FFT

    pilot_bits = [1, 1, 1, -1];
    X_pilot = pilot_bits + 0j; % Convert to complex symbols
    
    % Generate data tones (16-QAM modulation)
    % data_bits   = randi([0 mod_size - 1], length(data_idx), 1); % Random 16-QAM symbols
    % bit_golden  = int2bit(data_bits, log2(mod_size)); 
    bit_groups  = reshape(data_bits, log2(mod_size), []).';
    sym_indices = bi2de(bit_groups, 'left-msb');  % MSB first
    qam_mod     = qammod(sym_indices, mod_size, 'UnitAveragePower', true);

    % Create OFDM symbol in frequency domain
    ofdm_SYM            = zeros(N_FFT, 1);
    ofdm_SYM(data_idx)  = qam_mod;  % Assign QAM data
    ofdm_SYM(pilot_idx) = X_pilot; % Assign BPSK pilot tones
end