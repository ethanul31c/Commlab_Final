

I_data = iWave;
Q_data = qWave;
% I_pilot = real(Pilot_rx);
% Q_pilot = imag(Pilot_rx);

% ideal symbols
% ideal_symbols = qammod(0:QAM_size-1, QAM_size, 'gray', 'UnitAveragePower', true);
% Ii = real(ideal_symbols);
% Qi = imag(ideal_symbols);

% plot data and pilot
close all;
% figure(1);
% plot(I_pilot, Q_pilot, 'o','Color', '#939880', 'MarkerFaceColor', 'r', 'MarkerSize', 1); 
% hold on;
plot(I_data, Q_data, 'o', 'Color', '#875B75', 'MarkerFaceColor', 'r', 'MarkerSize', 1); 

% plot ideal symbol
% plot(Ii, Qi, 'x', 'Color', '#003C76', 'MarkerSize', 5, 'LineWidth', 1);
% I_bpsk = [1, -1];
% Q_bpsk = [0, 0];
% plot(I_bpsk, Q_bpsk, 'bx', 'MarkerSize', 5, 'LineWidth', 2); 


% axis([-1.5 1.5 -1.5 1.5]);
xlabel('I(t)');
ylabel('Q(t)');

xline(0, 'k', 'LineWidth', 1); % Real axis (vertical)
yline(0, 'k', 'LineWidth', 1); % Imaginary axis (horizontal)
legend({'received pilots', 'received data', 'ideal modulation'}, 'Location', 'northeast');
title('8. Received Constellation with CFO corrected');

axis equal;
grid on;
hold off;