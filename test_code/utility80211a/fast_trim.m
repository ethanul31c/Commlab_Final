% fast trim (may not be correct but faster)
function [sec_beg, sec_end] = fast_trim(buffer, plot_len, sec_blank)
    crt = 0.01;
    sec_beg = sec_blank;
    for ii = 1:length(buffer)
        if buffer(ii)>crt
            sec_beg = ii;
            break
        end
    end
    sec_beg = sec_beg - sec_blank + 1;
    sec_end = sec_beg + plot_len + 2*sec_blank;
end