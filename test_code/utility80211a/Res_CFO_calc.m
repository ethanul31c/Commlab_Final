function res_CFO_phase = Res_CFO_calc(Pilots, Q)
    res_CFO_phase = angle(sum(Pilots .* conj(Q)));
end