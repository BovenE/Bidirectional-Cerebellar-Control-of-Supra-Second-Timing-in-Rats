close all 
clear all 
my_dir = '/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Behaviour/Open_field_2';
d=dir([my_dir, '/*.xlsx']);
files={d.name};
distance_moved=zeros(9,1);
batch=2;
id_d=1;
id_c=1;
dist_c_10mins=zeros(6,1);
dist_c_5mins=zeros(6,1);
dist_d_10mins=zeros(6,1);
dist_d_5mins=zeros(6,1);

for k=1:numel(files)
    [num,txt,raw]=xlsread(fullfile(my_dir, files{k}));
    data_raw=num(:, 14:16);
    thresh = 0.1;
    degsmooth = 30; % number of points to average in moving mean calculation
%     %Open field 1 (these values are taken from measurements of the base)
%     upper_corner = [320 360];%will effect theactual distance ;%
%     lower_corner = [827 360];
    %Open field 2 (these values are taken from measurements of the base)
    upper_corner = [135 253];%will effect theactual distance ;%
    lower_corner = [480 253];
    fps = 30; % frames per second in video
    name = files{k}(10:17);
    [OFdata, results] = openFieldAnalysis(data_raw, thresh, degsmooth, upper_corner, lower_corner, name);
    tmp=split(files{k}, '_');
    rat=tmp{2}(2:end-3);
    rat_name=[rat(1:5), '_',rat(6:end)];
    [group_id]=get_groupid(batch, rat_name);
    disp(group_id);
    if group_id(1)=='C'
        dist_c_10mins(id_c) = results.dist_m_10mins;
        dist_c_5mins(id_c) = results.dist_m_5mins;
        id_c=id_c+1;
    else
        dist_d_10mins(id_d) = results.dist_m_10mins;
        dist_d_5mins(id_d) = results.dist_m_5mins;
        id_d=id_d+1;
    end
    xlim([300 900])
    ylim([100 700])
    text(750,650,['10mins ', num2str(round(results.dist_m_10mins, 3)), 'm']);
    text(750,625,['5mins ', num2str(round(results.dist_m_5mins, 3)), 'm']);
    saveas(gcf, [name, '.png']);
% distance_moved(k) = results.dist_m_10mins;
end

figure();
hold on
b=bar([1 2],[mean(dist_d_10mins) mean(dist_c_10mins)]);
errorbar([mean(dist_d_10mins) mean(dist_c_10mins)],[std(dist_d_10mins) std(dist_c_10mins)] ,'k.');
scatter(zeros(size(dist_d_10mins))+1, dist_d_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
scatter(zeros(size(dist_c_10mins))+2, dist_c_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
xticklabels({'DREADD', 'CONTROL'})
ylabel('Distance travelled 10mins (m)')
b.FaceColor = 'flat';
b.CData(1,:) = [.5 0 .5];
b.CData(2,:) = [.5 .5 .5];
xtickangle(45)
xticks([1 2])
[h,p,ci,stats] = ttest2(dist_d_10mins, dist_c_10mins)

figure();
hold on
b=bar([1 2],[mean(dist_d_5mins) mean(dist_c_5mins)])
errorbar([mean(dist_d_5mins) mean(dist_c_5mins)],[std(dist_d_5mins) std(dist_c_5mins)] ,'k.')
scatter(zeros(size(dist_d_5mins))+1, dist_d_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
scatter(zeros(size(dist_c_5mins))+2, dist_c_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
xticklabels({'DREADD', 'CONTROL'})
ylabel('Distance travelled 5mins (m)')
b.FaceColor = 'flat';
b.CData(1,:) = [.5 0 .5];
b.CData(2,:) = [.5 .5 .5];
xtickangle(45)
xticks([1 2])
[h,p,ci,stats] = ttest2(dist_d_10mins, dist_c_10mins)