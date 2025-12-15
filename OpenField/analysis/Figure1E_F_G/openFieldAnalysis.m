% Script to separate moving and non-moving segments in data
% Using TAIL BASE data for this analysis
% 22.04.2020
% BEFORE RUNNING SCRIPT
% 1. Load data as cell in 3 columns - x, y, likelihood - named data_raw (or take bit of code from old script if you can load all 3 columns of data in
% one go, I can't seem to do it in Matlab 2019a.
% 2. Need upper and lower corner coordinates of floor - allows for more accurate scaling
% 3. Set degree of smoothing - points to average for moving mean
% 4. Set threshold for separating moving/non moving. From prelim analysis 0.05 or 0.1 may be appropriate.

function [OFdata, results] = openFieldAnalysis(data_raw, thresh, degsmooth, upper_corner, lower_corner, name, open_field, do_plot);

disp('Processing ');
disp(name);
%thresh = 0.05;
%degsmooth =30; % number of points to average in moving mean calculation
upper_corner = upper_corner; %will effect theactual distance[480 333];%
disp(upper_corner);
lower_corner = lower_corner;
disp(lower_corner);
fps = 30; % frames per second in video

% EXTRACT DATA
% remove all the null/text values from within the dataset
%data = cell2mat(data_raw);
data = data_raw;
emptyvals = find(isnan(data));
emptyvals_indata = emptyvals <= length(data);
emptyvals = emptyvals(emptyvals_indata);
data(emptyvals,:) = [];

%extract 10 minutes of data (~18000 data points at 30 fps) from first point
%of high likelihood of detection
inOpenField = find(data(:,3) >= 0.99);
start = inOpenField(1);
OFdata = data(start:start + (fps*600), :); %10 minute data, 30 fps = 18000 data points
OFdata = data(inOpenField, :);
% figure()
% plot(OFdata(:,1), OFdata(:,2));
OFdata2=OFdata;
%%%%open field 2
if open_field ==2
    idx1=find(OFdata(:,1)>810);
    OFdata2(idx1,:)=[];
    inOpenField(idx1,:)=[];
    idx2=find(OFdata2(:,1)<=300);
    OFdata2(idx2,:)=[];
    inOpenField(idx2,:)=[];
    idx3=find(OFdata2(:,2)>550);
    inOpenField(idx3,:)=[];
    OFdata2(idx3,:)=[];
    idx4=find(OFdata2(:,2)>530 & OFdata2(:,1)>730);
    OFdata2(idx4,:)=[];
    inOpenField(idx4,:)=[];
    idx5=find(OFdata2(:,1)<550 & OFdata2(:,2)<228);
    OFdata2(idx5,:)=[];
    inOpenField(idx5,:)=[];
    idx6=find(OFdata2(:,1)>715 & OFdata2(:,2)>540);
    OFdata2(idx6,:)=[];
    inOpenField(idx6,:)=[];
    idx7=find(OFdata2(:,2)<=200);
    OFdata2(idx7,:)=[];
    inOpenField(idx7,:)=[];
end

%%%%open field 1
if open_field ==1
    idx1 = find(OFdata(:,1)>850);
    OFdata2(idx1,:)=[];
    inOpenField(idx1,:)=[];
    idx2 = find(OFdata2(:,1)<=300);
    OFdata2(idx2,:)=[];
    inOpenField(idx2,:)=[];
    disp(inOpenField(1)/30)
end

if do_plot
    plot(OFdata2(:,1), OFdata2(:,2));
    title(name);
end
OFdata=OFdata2;
% results=OFdat2;



%%
% % calculate total distance travelled in 10 min
d = hypot(diff(OFdata(:,1)), diff(OFdata(:,2))); % calculate distance between consecutive positions in pixels
d_tot = sum(d); % total distance in pixels
pixels = hypot(lower_corner(1) - upper_corner(1), lower_corner(2) - upper_corner(2));
scaling = 0.9/pixels;%the open field is 90cm at the bottom%1.4/pixels; %corner to corner of base is approx 1.4 metres - gives scaling in m
distance_m_10mins = d_tot * scaling;
distance_m_5mins = sum(d(1:(fps*300))) * scaling; % 9000 data points for 5 mins

%time = 1/fps:1/fps:length(d)/fps; %for plotting distance over time
d_smooth = movmean(d*(scaling*100),degsmooth); %smoothing and converting to cm instead of m for thresholding moving/non moving segs
[peakValues, indexesOfPeaks] = findpeaks(-d_smooth);
sortedPeaks=sort(-peakValues);
%thresh =mean(sortedPeaks(1:1000));

%%
%add code to plot over time 
av_dist_min=NaN(1,10);
timepoints=[0:60:600];
time=inOpenField/30;
for i=1:length(av_dist_min)
    av_dist_min(i)=sum(d(find(time(2:end)>timepoints(i) & time(2:end)<=timepoints(i+1))))* (scaling*100);
    
end

%%

%FIND START TIMES of moving segments
cross_m = find(d_smooth > thresh);
moving = zeros(size(d_smooth,1),1);

% start of moving segment marked by 1 - detected when changes to moving state
if cross_m(1) == 1 % if starts with moving segment, mark this from first data point
    moving(1) = 1;
end
for k = 2:size(cross_m,1)
    a = cross_m(k) == cross_m(k-1)+1;
    if a == 0
        moving(cross_m(k)) = 1;
    end
end

start_mov = time(find(moving))';

% START TIMES for stop segments
cross_s = find(d_smooth < thresh);
stopping = zeros(size(d_smooth,1),1);

% start of stopping segment = 1 (change of state from moving)
if cross_s(1) == 1 % does the recording start with a moving or stopping segment? 
    stopping(1) = 1;
else
    stopping(cross_s(1)) = 1;
end
for k = 2:size(cross_s,1)
    a = cross_s(k) == cross_s(k-1)+1;
    if a == 0
        stopping(cross_s(k)) = 1;
    end
end

stop_mov = time(find(stopping))';


% EXTRACT WINDOWS for both moving and stopping segments - need to test for
% unequal number of moving/stopping segments
movSegs = [];
stopSegs = [];

if length(start_mov) == length(stop_mov) % if same number of start/stop time points
    
    if start_mov(1) < stop_mov(1) % if recording starts with a moving segment
        movSegs(:,1) = start_mov;
        movSegs(:,2) = stop_mov;
        stopSegs(:,1) = stop_mov;
        stopSegs(1:size(stopSegs,1)-1,2) = start_mov(2:size(stopSegs,1));
        stopSegs(size(stopSegs,1),2) = max(time);
    end
    
    else if stop_mov(1) < start_mov(1) % if recording starts with a stopping segment - HAVE NOT TESTED SECTIONS FROM HERE
        stopSegs(:,1) = stop_mov;
        stopSegs(1:size(stopSegs,1)-1,2) = start_mov;
        movSegs(:,1) = start_mov;
        movSegs(1:size(stopSegs,1)-1,2) = stop_mov(2:length(stop_mov));
        movSegs(size(movSegs,1),2) = max(time);
        end
end

if length(start_mov) > length(stop_mov) % if more moving segments, starts and ends with moving segment
    movSegs(:,1) = start_mov;
    movSegs(1:length(stop_mov),2) = stop_mov;
    movSegs(length(movSegs),2) = max(time);
    stopSegs(:,1) = stop_mov;
    stopSegs(:,2) = start_mov(2:length(start_mov));
end
    
    
if length(start_mov) < length(stop_mov) % if more stopping segments, starts and ends with stopping segment
     movSegs(:,1) = start_mov;
     movSegs(:,2) = stop_mov(2:length(stop_mov));
     stopSegs(:,1) = stop_mov;
     stopSegs(1:length(start_mov),2) = start_mov;
     stopSegs(length(stopSegs),2) = max(time);
end

% PLOT smoothed distance data with moving segments labelled by red line
if do_plot
    figure()
    plot(time(2:end),d_smooth,'k')
    hold on
    y = [1 1];
    for k = 1:size(movSegs,1)
        line(movSegs(k,:),y, 'Color', 'red', 'LineWidth', 1)
    end
    ylim([0 1.1])
    % add threshold line
    x = [time(1) time(size(time,2))];
    y = [thresh thresh];
    line(x,y)
    xlabel('Time (secs)')
    ylabel('Smoothed distance (cm/s)')
    legend('Distance', 'Moving segments')
end
% QUANTIFY moving segments
number_moving = size(movSegs,1);
length_moving = movSegs(:,2) - movSegs(:,1);
mean_length_moving = mean(length_moving);
median_length_moving = median(length_moving);

% QUANTIFY stop segments
number_stopping = size(stopSegs,1);
length_stopping = stopSegs(:,2) - stopSegs(:,1);
mean_length_stopping = mean(length_stopping);
median_length_stopping = median(length_stopping);

% AVERAGE VELOCITY in moving segments
% d_moving = cell(1,length(movSegs)); % empty cell array to hold each segment
% d_velocity = zeros(1,length(movSegs));
t = 1/fps;
% 
% for k = 1:length(movSegs)
%     isolatedSeg = find(time >= movSegs(k,1) & time <= movSegs(k,2));
%     d_moving{k} = d(isolatedSeg(1):isolatedSeg(length(isolatedSeg)));
%     d_velocity(k) = mean(((d_moving{k}*scaling)*100)/t); % distance divided by time for each data point; * 100 to get scaled data in cm/s
% end
% 
% avg_velocity_moving = mean(d_velocity);

%overall average velocity
tot_avg_vel10min = mean(((d*scaling)*100)/t);
tot_avg_vel5min = mean(((d(1:(fps*300))*scaling)*100)/t);

if do_plot
    figure()
    plot(OFdata(:,1)* scaling, OFdata(:,2)* scaling, 'k');
end 
results.dist_m_10mins = distance_m_10mins;
results.dist_m_5mins = distance_m_5mins;
results.tot_avg_vel10min =tot_avg_vel10min;
results.tot_avg_vel5min =tot_avg_vel5min;
results.number_moving = number_moving; 
results.number_stopping = number_stopping;
results.mean_length_moving =mean_length_moving;
results.median_length_moving =median_length_moving;
results.median_length_stopping =median_length_stopping;
%results.avg_velocity_moving = avg_velocity_moving;
results.avg_dist_min = av_dist_min;

disp('RESULTS')
disp(['total distance in 10 min = ', num2str(distance_m_10mins), ' metres']);
disp(['total distance in 5 min = ', num2str(distance_m_5mins), ' metres']);
disp(['overall average velocity in 10 min = ', num2str(tot_avg_vel10min), ' cm/s']);
disp(['overall average velocity in 5 min = ', num2str(tot_avg_vel5min), ' cm/s']);
disp(['number moving segments = ', num2str(number_moving)]);
disp(['number stopping segments = ', num2str(number_stopping)]);
disp(['mean length moving = ', num2str(mean_length_moving), ' seconds']);
disp(['median length moving = ', num2str(median_length_moving), ' seconds']);
disp(['mean length stopping = ', num2str(mean_length_stopping), ' seconds']);
disp(['median length stopping = ', num2str(median_length_stopping), ' seconds']);
%disp(['mean velocity moving segments = ', num2str(avg_velocity_moving), ' cm/s']);

end 
