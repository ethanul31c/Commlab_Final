K = 100;
QAM_size = 16;

if QAM_size == 16
    rate = [1 0 1 1]
elseif QAM_size == 64
    rate = [0 0 1 1]
end
P = 1
zero_tail = zeros(1, 12); 
K = de2bi(K, 12, "right-msb");
M = [rate, 0, K, P, zero_tail]

rate = '1/2';
LSIG_tx = wlanBCCEncode(M.',rate);
LSIG_tx = LSIG_tx(1:48);


LSIG_rx = [LSIG_tx(1:48); zeros(12, 1)]
LSIG_rx = wlanBCCDecode(LSIG_rx, rate, 'hard')
LSIG_rx = LSIG_rx(1:24).'

a = sum(M(1:24) ~= LSIG_rx)