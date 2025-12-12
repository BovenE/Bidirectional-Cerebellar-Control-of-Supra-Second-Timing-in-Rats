close all 
clear all 
dir_openfield1 = '/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Behaviour/Open_field';
dir_openfield2 = '/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Behaviour/Open_field_2';

dir1=dir([dir_openfield1, '/*.xlsx']);
files_openfield1={dir1.name};

dir2=dir([dir_openfield2, '/*.xlsx']);
files_openfield2={dir2.name};

distance_moved=zeros(9,1);
batch=2;
id_d=1;
id_c=1;
dist_c_10mins=zeros(6,1);
dist_c_5mins=zeros(6,1);
number_c_moving1=zeros(6,1);
number_c_moving2=zeros(6,1);

dist_d_10mins=zeros(6,1);
dist_d_5mins=zeros(6,1);
number_d_moving1=zeros(6,1);
number_d_moving2=zeros(6,1);



if length(files_openfield1)==length(files_openfield2)
    n_files =length(files_openfield1);
else
    disp('not equal number of animals in openfield 1 versus open field 2')
    quit
end
for k=1%n_files
    %read in open field 1 data 
    [num1,txt1,raw1]=xlsread(fullfile(dir_openfield1, files_openfield1{k}));
    data_raw1=num1(:, 14:16);
    
    [num2,txt2,raw2]=xlsread(fullfile(dir_openfield2, files_openfield2{k}));
    data_raw2=num2(:, 14:16);
    
    thresh = 0.1;
    degsmooth = 60; % number of points to average in moving mean calculation
%     %Open field 1 (these values are taken from measurements of the base)
    upper_corner1 = [320 360];%will effect theactual distance ;%
    lower_corner1 = [827 360];
    %Open field 2 (these values are taken from measurements of the base)
    upper_corner2 = [135 253];%will effect theactual distance ;%
    lower_corner2 = [480 253];
    fps = 30; % frames per second in video
    name1 = files_openfield1{k}(10:17);
    name2 = files_openfield2{k}(10:17);

    
    if strcmp(name1, name2)
        [OFdata_openfield_1, results_openfield1] = openFieldAnalysis(data_raw1, thresh, degsmooth, upper_corner1, lower_corner1, name1, 1, 1);
        pause()
        [OFdata_openfield_2, results_openfield2] = openFieldAnalysis(data_raw2, thresh, degsmooth, upper_corner2, lower_corner2, name2, 2, 1);
        pause()
        tmp=split(files_openfield1{k}, '_');
        rat=tmp{2}(2:end-3);
        rat_name=[rat(1:5), '_',rat(6:end)];
        [group_id]=get_groupid(batch, rat_name);
        disp(group_id);
        
    else
        disp('Processing two different animals for openfield 1 and openfield 2, EXIT');
        quit
    end


    if group_id(1)=='C'
        dist1_c_10mins(id_c) = results_openfield1.median_length_stopping;%results_openfield1.dist_m_10mins;
        dist1_c_5mins(id_c) = results_openfield1.avg_velocity_moving;%results_openfield1.dist_m_5mins;
        dist2_c_10mins(id_c) = results_openfield2.median_length_stopping;%results_openfield2.dist_m_10mins;
        dist2_c_5mins(id_c) = results_openfield2.avg_velocity_moving;%results_openfield2.dist_m_5mins;
        number_c_moving1(id_c) = results_openfield1.mean_length_moving; %results_openfield1.number_moving;
        number_c_moving2(id_c) = results_openfield2.mean_length_moving;%results_openfield2.number_moving;

        id_c=id_c+1;
    else
        dist1_d_10mins(id_c) = results_openfield1.median_length_stopping;%results_openfield1.dist_m_10mins;
        dist1_d_5mins(id_c) = results_openfield1.avg_velocity_moving;%results_openfield1.dist_m_5mins;
        dist2_d_10mins(id_c) = results_openfield2.median_length_stopping;%results_openfield2.dist_m_10mins;
        dist2_d_5mins(id_c) = results_openfield2.avg_velocity_moving;%results_openfield2.dist_m_5mins;
        number_d_moving1(id_c) = results_openfield1.mean_length_moving; %results_openfield1.number_moving;
        number_d_moving2(id_c) = results_openfield2.mean_length_moving;%results_openfield2.number_moving;

        id_d=id_d+1;
    end
%     xlim([300 900])
%     ylim([100 700])
%     text(750,650,['10mins ', num2str(round(results.dist_m_10mins, 3)), 'm']);
%     text(750,625,['5mins ', num2str(round(re1sults.dist_m_5mins, 3)), 'm']);
%     saveas(gcf, [name, '.png']);
% distance_moved(k) = results.dist_m_10mins;
end

% figure();
% hold on
% b=bar([1 2 3 4],[mean(dist1_c_10mins) mean(dist2_c_10mins) mean(dist1_d_10mins) mean(dist2_d_10mins)]);
% errorbar([mean(dist1_c_10mins) mean(dist2_c_10mins) mean(dist1_d_10mins) mean(dist2_d_10mins)],[std(dist1_c_10mins) std(dist2_c_10mins) std(dist1_d_10mins) std(dist2_d_10mins)] ,'k.');
% scatter(zeros(size(dist1_c_10mins))+1, dist1_c_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_c_10mins))+2, dist2_c_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(dist1_c_10mins))+1; zeros(size(dist2_c_10mins))+2], [dist1_c_10mins; dist2_c_10mins], 'Color', 'k')
% scatter(zeros(size(dist1_d_10mins))+3, dist1_d_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_d_10mins))+4, dist2_d_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(dist1_d_10mins))+3; zeros(size(dist2_d_10mins))+4], [dist1_d_10mins; dist2_d_10mins], 'Color', 'k')
% 
% xticklabels({'Control 1', 'Control 2', 'DREADD 1', 'DREADD 2'})
% %ylabel('Distance travelled 10mins (m)')
% ylabel('Median stopping length (s)');
% b.FaceColor = 'flat';
% b.CData(3,:) = [.5 0 .5];
% b.CData(4,:) = [.5 0 .5];
% 
% b.CData(1,:) = [.5 .5 .5];
% b.CData(2,:) = [.5 .5 .5];
% 
% xtickangle(45)
% xticks([1 2 3 4])
% title('Open field 1')
% %[h,p,ci,stats] = ttest2(dist1_d_10mins, dist2_d_10mins)
% 
% 
% 
% figure();
% hold on
% b=bar([1 2 3 4],[mean(dist1_c_5mins) mean(dist2_c_5mins) mean(dist1_d_5mins) mean(dist2_d_5mins)]);
% errorbar([mean(dist1_c_5mins) mean(dist2_c_5mins) mean(dist1_d_5mins) mean(dist2_d_5mins)],[std(dist1_c_5mins) std(dist2_c_5mins) std(dist1_d_5mins) std(dist2_d_5mins)] ,'k.');
% scatter(zeros(size(dist1_c_5mins))+1, dist1_c_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_c_5mins))+2, dist2_c_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(dist1_c_5mins))+1; zeros(size(dist2_c_5mins))+2], [dist1_c_5mins; dist2_c_5mins], 'Color', 'k')
% scatter(zeros(size(dist1_d_5mins))+3, dist1_d_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_d_5mins))+4, dist2_d_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(dist1_d_5mins))+3; zeros(size(dist2_d_5mins))+4], [dist1_d_5mins; dist2_d_5mins], 'Color', 'k')
% 
% xticklabels({'Control 1', 'Control 2', 'DREADD 1', 'DREADD 2'})
% %ylabel('Distance travelled 5mins (m)')
% ylabel('Average velocity (cm/s)');
% b.FaceColor = 'flat';
% b.CData(3,:) = [.5 0 .5];
% b.CData(4,:) = [.5 0 .5];
% 
% b.CData(1,:) = [.5 .5 .5];
% b.CData(2,:) = [.5 .5 .5];
% 
% xtickangle(45)
% xticks([1 2 3 4])
% [h,p,ci,stats] = ttest2(dist1_d_5mins, dist2_d_5mins)
% 
% figure();
% hold on
% b=bar([1 2],[mean(dist1_c_5mins) mean(dist1_d_5mins)])
% errorbar([mean(dist1_c_5mins) mean(dist1_d_5mins)],[std(dist1_c_5mins) std(dist1_d_5mins)] ,'k.')
% scatter(zeros(size(dist1_c_5mins))+1, dist1_c_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist1_d_5mins))+2, dist1_d_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% %ylabel('Distance travelled 5mins (m)')
% ylabel('Average velocity')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% title('Open field 1')
% [h,p,ci,stats] = ttest2(dist1_d_5mins, dist1_c_5mins)
% 
% 
% figure();
% hold on
% b=bar([1 2],[mean(dist1_c_10mins) mean(dist1_d_10mins)])
% errorbar([mean(dist1_c_10mins) mean(dist1_d_10mins)],[std(dist1_d_10mins) std(dist1_d_10mins)] ,'k.')
% scatter(zeros(size(dist1_c_10mins))+1, dist1_c_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist1_d_10mins))+2, dist1_d_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% ylabel('Median stopping length')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% title('Open field 1')
% [h,p,ci,stats] = ttest2(dist1_d_10mins, dist1_c_10mins)
% 
% 
% 
% figure();
% hold on
% b=bar([1 2],[mean(dist2_c_5mins) mean(dist2_d_5mins)])
% errorbar([mean(dist2_c_5mins) mean(dist2_d_5mins)],[std(dist2_c_5mins) std(dist2_d_5mins)] ,'k.')
% scatter(zeros(size(dist2_c_5mins))+1, dist2_c_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_d_5mins))+2, dist2_d_5mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% %ylabel('Distance travelled 5mins (m)')
% ylabel('average velocity (cm/s)')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% [h,p,ci,stats] = ttest2(dist2_d_10mins, dist2_c_10mins)
% title('Open field 2')
% 
% 
% figure();
% hold on
% b=bar([1 2],[mean(dist2_c_10mins) mean(dist2_d_10mins)])
% errorbar([mean(dist2_c_10mins) mean(dist2_d_10mins)],[std(dist2_c_10mins) std(dist2_d_10mins)] ,'k.')
% scatter(zeros(size(dist2_c_10mins))+1, dist2_c_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(dist2_d_10mins))+2, dist2_d_10mins, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% %ylabel('Distance travelled 10mins (m)')
% ylabel('Median stopping length')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% title('Open field 2')
% [h,p,ci,stats] = ttest2(dist2_d_10mins, dist2_c_10mins)
% 
% 
% % PLotting for movement segments
% figure();
% hold on
% openfieldA=number_c_moving1;
% openfieldB=number_d_moving1;
% b=bar([1 2],[mean(openfieldA) mean(openfieldB)])
% errorbar([mean(openfieldA) mean(openfieldB)],[std(openfieldA) std(openfieldB)] ,'k.')
% scatter(zeros(size(openfieldA))+1, openfieldA, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfieldB))+2,openfieldB, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% %ylabel('Distance travelled 10mins (m)')
% ylabel('Median movinglength')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% title('Open field 1')
% [h,p,ci,stats] = ttest2(openfieldA, openfieldB)
% 
% 
% % PLotting for movement segments
% figure();
% hold on
% openfieldA=number_c_moving2;
% openfieldB=number_d_moving2;
% b=bar([1 2],[mean(openfieldA) mean(openfieldB)]);
% errorbar([mean(openfieldA) mean(openfieldB)],[std(openfieldA) std(openfieldB)] ,'k.');
% scatter(zeros(size(openfieldA))+1, openfieldA, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfieldB))+2,openfieldB, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'});
% %ylabel('Distance travelled 10mins (m)');
% ylabel('Median moving length')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45);
% xticks([1 2]);
% title('Open field 2');
% [h,p,ci,stats] = ttest2(openfieldA, openfieldB);
% 
% 
% 
% %moving segments
% openfield1_c=number_c_moving1;
% openfield1_d=number_d_moving1;
% openfield2_c=number_c_moving2;
% openfield2_d=number_d_moving2;
% figure();
% hold on
% b=bar([1 2 3 4],[mean(openfield1_c) mean(openfield2_c) mean(openfield2_d) mean(openfield1_d)]);
% errorbar([mean(openfield1_c) mean(openfield2_c) mean(openfield2_d) mean(openfield1_d)],[std(openfield1_c) std(openfield2_c) std(openfield1_d) std(openfield2_d)] ,'k.');
% scatter(zeros(size(openfield1_c))+1, openfield1_c, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfield2_c))+2, openfield2_c, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(openfield1_c))+1; zeros(size(openfield2_c))+2], [openfield1_c; openfield2_c], 'Color', 'k')
% scatter(zeros(size(openfield1_d))+3, openfield1_d, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfield2_d))+4, openfield2_d, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(openfield1_d))+3; zeros(size(openfield2_d))+4], [openfield1_d; openfield2_d], 'Color', 'k')
% 
% xticklabels({'Control 1', 'Control 2', 'DREADD 1', 'DREADD 2'})
% %ylabel('Distance travelled 10mins (m)')
% ylabel('Median movement length');
% b.FaceColor = 'flat';
% b.CData(3,:) = [.5 0 .5];
% b.CData(4,:) = [.5 0 .5];
% 
% b.CData(1,:) = [.5 .5 .5];
% b.CData(2,:) = [.5 .5 .5];
% 
% xtickangle(45)
% xticks([1 2 3 4])
% 
% 
% % PLotting for movement segments
% figure();
% hold on
% openfieldA=number_c_moving1;
% openfieldB=number_d_moving1;
% b=bar([1 2],[mean(openfieldA) mean(openfieldB)])
% errorbar([mean(openfieldA) mean(openfieldB)],[std(openfieldA) std(openfieldB)] ,'k.')
% scatter(zeros(size(openfieldA))+1, openfieldA, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfieldB))+2,openfieldB, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'CONTROL', 'DREADD'})
% %ylabel('moving bouts (count)')
% ylabel('Median moving length')
% b.FaceColor = 'flat';
% b.CData(2,:) = [.5 0 .5];
% b.CData(1,:) = [.5 .5 .5];
% xtickangle(45)
% xticks([1 2])
% title('Open field 1')
% [h,p,ci,stats] = ttest2(openfieldA, openfieldB)
% 
% 
% % PLotting for movement segments
% figure();
% hold on
% openfieldA=number_c_moving2;
% openfieldB=number_d_moving2;
% b=bar([1 2],[mean(openfieldA) mean(openfieldB)]);
% errorbar([mean(openfieldA) mean(openfieldB)],[std(openfieldA) std(openfieldB)] ,'k.');
% scatter(zeros(size(openfieldA))+1, openfieldA, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfieldB))+2,openfieldB, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% xticklabels({'DREADD', 'CONTROL'});
% %ylabel('moving bouts (count)')
% ylabel('Median moving length')
% b.FaceColor = 'flat';
% b.CData(1,:) = [.5 0 .5];
% b.CData(2,:) = [.5 .5 .5];
% xtickangle(45);
% xticks([1 2]);
% title('Open field 2');
% [h,p,ci,stats] = ttest2(openfieldA, openfieldB);
% 
% 
% 
% %moving segments
% openfield1_c=number_c_moving1.';
% openfield1_d=number_d_moving1.';
% openfield2_c=number_c_moving2.';
% openfield2_d=number_d_moving2.';
% figure();
% hold on
% b=bar([1 2 3 4],[mean(openfield1_c) mean(openfield2_c) mean(openfield1_d) mean(openfield2_d)]);
% errorbar([mean(openfield1_c) mean(openfield2_c) mean(openfield1_d) mean(openfield2_d)],[std(openfield1_c) std(openfield2_c) std(openfield1_d) std(openfield2_d)] ,'k.');
% scatter(zeros(size(openfield1_c))+1, openfield1_c, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfield2_c))+2, openfield2_c, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(openfield1_c))+1; zeros(size(openfield2_c))+2], [openfield1_c; openfield2_c], 'Color', 'k')
% scatter(zeros(size(openfield1_d))+3, openfield1_d, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% scatter(zeros(size(openfield2_d))+4, openfield2_d, 'MarkerFaceColor', [0 .7 .7], 'MarkerEdgeColor', [0 .7 .7])
% line([zeros(size(openfield1_d))+3; zeros(size(openfield2_d))+4], [openfield1_d; openfield2_d], 'Color', 'k')
% xticklabels({'CONTROL 1', 'CONTROL 2', 'DREADD 1', 'DREADD 2'});
% %ylabel('moving bouts (count)')
% ylabel('Median moving length')
% b.FaceColor = 'flat';
% b.CData(1,:) = [.5 .5 .5];
% b.CData(2,:) = [.5 .5 .5];
% b.CData(3,:) = [.5 0 .5];
% b.CData(4,:) = [.5 0 .5];
% xtickangle(45);
% xticks([1 2]);
% title('Comparing open fields');
% [h,p,ci,stats] = ttest2(openfieldA, openfieldB);
