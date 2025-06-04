% Equalization
function  [Pilot, Data] = Equalize(Symbol, H) % freq domain
    global data_idx;
    global pilot_idx;
    Y = Symbol;

    Data = zeros(48, 1);
    Pilot = zeros(4, 1);

    data_nonzero_idx = data_idx(H(data_idx) ~= 0);

    Data = Y(data_idx)./H(data_idx);
    Pilot = Y(pilot_idx)./H(pilot_idx);
end