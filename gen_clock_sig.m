clear;
close all;

t = linspace(-2, 8, 1000);
clock = @(t) square(2.*pi.*t);
SPI = @(t) (square(pi.*t)).*double(t>=0);
SPIu = @(t) (square(pi.*(t-0.25))).*double((t-0.25)>= 0);

figure('Name', 'SPI Sync');
subplot(2,1,1);
plot(t, SPI(t), 'Color', [0,0,0]);
title('Synchronized SPI Signal');
grid on;
xlabel('Time');
axis([-2 8 -2 2])
subplot(2,1,2);
plot(t, clock(t), 'Color', [0,0,0]);
title('Clock');
grid on;
xlabel('Time');
axis([-2 8 -2 2])

figure('Name', 'SPI Unsync', 'Color', [1,1,1]);
subplot(2,1,1);
plot(t, SPIu(t), 'Color', [0,0,0]);
title('Unsynchronized SPI Signal');
grid on;
xlabel('Time');
axis([-2 8 -2 2])
subplot(2,1,2);
plot(t, clock(t), 'Color', [0,0,0]);
title('Clock');
grid on;
xlabel('Time');
axis([-2 8 -2 2])
