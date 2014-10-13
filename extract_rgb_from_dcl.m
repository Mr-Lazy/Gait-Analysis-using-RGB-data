
function extract_rgb_fromdcl(training_set,number_of_frame,flag_test)
    tic
    data = textread(training_set,'%s');
    NUI_SKELETON_TRACKED = 2;
    NUI_SKELETON_POSITION_ONLY = 1;
    NUI_SKELETON_COUNT = 6;
    %mkdir(strcat('features'));
    mkdir(strcat('rgbfeatures'));
    mkdir(strcat('rgbtestfeatures'));
     if flag_test==0
       disp('extracting_information out of training data in extract joints_binary');
     for iii=1:numel(data)/4
             flag_gait_cycle=0;
   
    fid = fopen(data{4*iii-3});
    %mkdir(strcat('features\',data{4*iii-2}));
    %path = strcat('features\',data{4*iii-2},'\');
    mkdir(strcat('rgbfeatures\',data{4*iii-2}));
    path_rgb = strcat('rgbfeatures\',data{4*iii-2},'\');
    
    
    %Header information
    firstdata = fread(fid,1,'uint32');
    versionRead =  bitshift(firstdata, -8);
    nStream =  bitand(firstdata , 000000000000000000000000000000011);
    
    streamIDcolor = fread(fid,1,'uint32');
    Heightcolor = fread(fid,1,'uint32');
    Weidthcolor = fread(fid,1,'uint32');
    BytePerPixelcolor = fread(fid,1,'uint32');
    streamIDDepth = fread(fid,1,'uint32');
    HeightDepth = fread(fid,1,'uint32');
    WeidthDepth = fread(fid,1,'uint32');
    BytePerPixelDepth = fread(fid,1,'uint32');
    if nStream == 3
        streamIDskeleton = fread(fid,1,'uint32');
    end
    
    FrameNumber = 0;
   
        
    count = 0;
    count1=0;
      while ~feof(fid)
        StreamID = fread(fid,1,'uint32');
                        
        if StreamID == 2
            %Color Stream
            timeStampC = fread(fid,1,'uint64');
            FramNumberC = fread(fid,1,'uint32');
            ColorStream = fread(fid,Heightcolor*Weidthcolor*BytePerPixelcolor,'uint8');

            z=0;

            rgbimage = zeros(Heightcolor,Weidthcolor,3);
            for i = 1:Heightcolor
                for j = 1:Weidthcolor
                    for k = 1:BytePerPixelcolor-1
                        z = z+1;
                        rgbimage(i,j,k) = ColorStream(z);
                    end
                    z=z+1;
                end
            end
            %BGR to RGB matrix 
            rgbtemp = zeros(Heightcolor,Weidthcolor,3);
            rgbtemp(:,:,1)=  rgbimage(:,:,1);
            rgbimage(:,:,1)= rgbimage(:,:,3);
            rgbimage(:,:,3)= rgbtemp(:,:,1);

            %matrix to gray image
            rgbimage(:,:,1) = fliplr(mat2gray(rgbimage(:,:,1)));
            rgbimage(:,:,2) = fliplr(mat2gray(rgbimage(:,:,2)));
            rgbimage(:,:,3) = fliplr(mat2gray(rgbimage(:,:,3)));
            %rgbimage = fliplr(rgbimage);
           
            if FrameNumber 
                if  count < 500
                    %rgbimage = imresize(rgbimage,[240 320]);
                     %imwrite(rgbimage,[int2str(count),'.jpg']);
                     filename=sprintf('%03d',count);
                     imwrite(rgbimage,strcat(path_rgb,filename,'.jpeg'));
                end
            end
            
        elseif StreamID == 1
        %Depth Stream
            timeStampD = fread(fid,1,'uint64');
            FramNumberD = fread(fid,1,'uint32');
            DepthStream = fread(fid, HeightDepth*WeidthDepth,'uint16');
       
            FrameNumber = FramNumberD;
            
            %Depth = reshape(DepthStream, HeightDepth, WeidthDepth);
            Depth = reshape(DepthStream, WeidthDepth, HeightDepth);

            %Shifting 3bit player I
            B = bitshift(Depth, -3);
            B = rot90(B, -1);
            
            [r c] = size(B);
                       
            for i = 1:r    %top:240 - bottom
                for j = 1:c    %left:320 - right
                    if B(i, j) >= 4095
                        B(i, j) = 0;
                    end
                end
            end
            

            
            maxVal = max(B(:));
            minVal = min(B(:));
      
            diff = maxVal - minVal;
            range = double(255)/double(diff);

            depthImage = zeros(r, c);

            for i=1: HeightDepth 
               for j = 1:WeidthDepth
                   intVal = range * (B(i,j) - minVal);
                   depthImage(i, j) = intVal;

               end
            end
            I = mat2gray(depthImage);  
            %imshow(I)
            %I = fliplr(I);
                                                            
            count = count+1;
            if count == number_of_frame
                break;
            end
           
                %imwrite(I,strcat(path,num2str(count),'.png'));
                %B=imread(strcat(path,'1.png'));
                %A=imread(strcat(path,num2str(count),'.png'));
                %bw=im2bw(B-A, 0.05);
                %CC = bwconncomp(bw);
                %numPixels = cellfun(@numel,CC.PixelIdxList);
                %D=sort(numPixels);
                %if(numel(numPixels)>1)
                %E=D(numel(numPixels));
                %BW2 = bwareaopen(bw, E-1);
                %imwrite(BW2,strcat(path,'bw_',num2str(count),'.png'));
                %else
                    %imwrite(bw,strcat(path,'bw_',num2str(count),'.png'));
                %end
            %end
            
        %Skeleton stream    
        else
            % disp('00');
            %trackingState = fread(fid,1,'uint32');
            if versionRead == 1
                liTimeStamp = fread(fid,1 ,'uint64');	
                dwFrameNumber = fread(fid,1,'uint32');	
                vFloorClipPlane = fread(fid,4,'uint32'); 
                %vFloorClipPlane = fread(fid,16); 
            end
            for i = 1:NUI_SKELETON_COUNT
              %  disp('01');
                eTrackingState = fread(fid,1,'uint32');	
                if eTrackingState == NUI_SKELETON_TRACKED
               %     disp('02');
                    dwTrackingID = fread(fid,1,'uint32');	
                    dwEnrollmentIndex = fread(fid,1,'uint32');	
                    dwUserIndex = fread(fid,1,'uint32');	
                    Position = fread(fid,4,'float');
                    count1=count1+1;
                     if flag_gait_cycle==0
                     %debugSkeletonLogFP3 = fopen('joint_tracking_training.txt','a+');
                     %fprintf(debugSkeletonLogFP3,'%s %d\n' ,data{4*iii-2},count);
                     %fclose(debugSkeletonLogFP3);
                     flag_gait_cycle=1;
                     end
                    %fprintf(debugSkeletonLogFP1,'TRACKED\n');
                    for k = 1:20
                        
                        SkeletonPositionsX = fread(fid,1,'float');	
                        SkeletonPositionsY = fread(fid,1,'float');	
                        SkeletonPositionsZ = fread(fid,1,'float');	
                        SkeletonPositionsW = fread(fid,1,'float');
                       
                        %debugSkeletonLogFP1 = fopen(strcat(path,'Joint_',int2str(k),'.txt'),'a+');
                        %fprintf(debugSkeletonLogFP1,' %f, %f, %f, %f\n' ,SkeletonPositionsX, SkeletonPositionsY, SkeletonPositionsZ,SkeletonPositionsW);
						%fclose(debugSkeletonLogFP1);
                        if k==15
                            ankle_left_posX = SkeletonPositionsX;
                        end
                        if k==20
                            ankle_right_posX = SkeletonPositionsX;
                        end
                          
                    end
                      
                        %debugSkeletonLogFP2 = fopen(strcat(path,'diff.txt'),'a+');
                        %fprintf(debugSkeletonLogFP2,' %f\n' ,abs(ankle_left_posX-ankle_right_posX));
						%fclose(debugSkeletonLogFP2);
                    eSkeletonPositionTrackingState = fread(fid,20 ,'uint32');	
                    dwQualityFlags = fread(fid,1,'uint32');	
                elseif eTrackingState == NUI_SKELETON_POSITION_ONLY
                   
                    PositionX = fread(fid,1,'float');	
                    PositionY = fread(fid,1,'float');	
                    PositionZ = fread(fid,1,'float');	
                    PositionW = fread(fid,1,'float');	
                   
                end
                              
            end
           
                              
        end
           
      end
    fclose(fid);
    %fclose(fid_m);
   
         end
         
     else
      disp('extracting_information out of test data in extract joints_binary');
      for iii=1:numel(data)/2
             flag_gait_cycle=0;
   
    fid = fopen(data{2*iii-1});
    %mkdir( strcat('features\',data{2*iii}));
    %path = strcat('features\',data{2*iii},'\');
    mkdir(strcat('rgbtestfeatures\',data{2*iii}));
    path_rgb = strcat('rgbtestfeatures\',data{2*iii},'\');
    
    
    %Header information
    firstdata = fread(fid,1,'uint32');
    versionRead =  bitshift(firstdata, -8);
    nStream =  bitand(firstdata , 000000000000000000000000000000011);
    
    streamIDcolor = fread(fid,1,'uint32');
    Heightcolor = fread(fid,1,'uint32');
    Weidthcolor = fread(fid,1,'uint32');
    BytePerPixelcolor = fread(fid,1,'uint32');
    streamIDDepth = fread(fid,1,'uint32');
    HeightDepth = fread(fid,1,'uint32');
    WeidthDepth = fread(fid,1,'uint32');
    BytePerPixelDepth = fread(fid,1,'uint32');
    if nStream == 3
        streamIDskeleton = fread(fid,1,'uint32');
    end
    
    FrameNumber = 0;
   
        
    count = 0;
    count1=0;
      while ~feof(fid)
        StreamID = fread(fid,1,'uint32');
                        
        if StreamID == 2
            %Color Stream
            timeStampC = fread(fid,1,'uint64');
            FramNumberC = fread(fid,1,'uint32');
            ColorStream = fread(fid,Heightcolor*Weidthcolor*BytePerPixelcolor,'uint8');

            z=0;

            rgbimage = zeros(Heightcolor,Weidthcolor,3);
            for i = 1:Heightcolor
                for j = 1:Weidthcolor
                    for k = 1:BytePerPixelcolor-1
                        z = z+1;
                        rgbimage(i,j,k) = ColorStream(z);
                    end
                    z=z+1;
                end
            end
            %BGR to RGB matrix 
            rgbtemp = zeros(Heightcolor,Weidthcolor,3);
            rgbtemp(:,:,1)=  rgbimage(:,:,1);
            rgbimage(:,:,1)= rgbimage(:,:,3);
            rgbimage(:,:,3)= rgbtemp(:,:,1);

            %matrix to gray image
            rgbimage(:,:,1) = fliplr(mat2gray(rgbimage(:,:,1)));
            rgbimage(:,:,2) = fliplr(mat2gray(rgbimage(:,:,2)));
            rgbimage(:,:,3) = fliplr(mat2gray(rgbimage(:,:,3)));
            %rgbimage = fliplr(rgbimage);
           
            if FrameNumber 
                if  count < 500
                    %rgbimage = imresize(rgbimage,[240 320]);
                     %imwrite(rgbimage,[int2str(count),'.jpg']);
                     filename=sprintf('%03d',count);
                     imwrite(rgbimage,strcat(path_rgb,filename,'.jpeg'));
                end
            end
            
        elseif StreamID == 1
        %Depth Stream
            timeStampD = fread(fid,1,'uint64');
            FramNumberD = fread(fid,1,'uint32');
            DepthStream = fread(fid, HeightDepth*WeidthDepth,'uint16');
       
            FrameNumber = FramNumberD;
            
            %Depth = reshape(DepthStream, HeightDepth, WeidthDepth);
            Depth = reshape(DepthStream, WeidthDepth, HeightDepth);

            %Shifting 3bit player I
            B = bitshift(Depth, -3);
            B = rot90(B, -1);
            
            [r c] = size(B);
                       
            for i = 1:r    %top:240 - bottom
                for j = 1:c    %left:320 - right
                    if B(i, j) >= 4095
                        B(i, j) = 0;
                    end
                end
            end
            

            
            maxVal = max(B(:));
            minVal = min(B(:));
      
            diff = maxVal - minVal;
            range = double(255)/double(diff);

            depthImage = zeros(r, c);

            for i=1: HeightDepth 
               for j = 1:WeidthDepth
                   intVal = range * (B(i,j) - minVal);
                   depthImage(i, j) = intVal;

               end
            end
            I = mat2gray(depthImage);  
            %imshow(I)
            %I = fliplr(I);
                                                            
            count = count+1;
            if count == number_of_frame
                break;
            end
           
                %imwrite(I,strcat(path,num2str(count),'.png'));
                %B=imread(strcat(path,'1.png'));
                %A=imread(strcat(path,num2str(count),'.png'));
                %bw=im2bw(B-A, 0.05);
                %CC = bwconncomp(bw);
                %numPixels = cellfun(@numel,CC.PixelIdxList);
                %D=sort(numPixels);
                %if(numel(numPixels)>1)
                    %E=D(numel(numPixels));
                    %BW2 = bwareaopen(bw, E-1);
                    %imwrite(BW2,strcat(path,'bw_',num2str(count),'.png'));
                %else
                    %imwrite(bw,strcat(path,'bw_',num2str(count),'.png'));
                %end
            %end
            
        %Skeleton stream    
        else
             %disp('00');
            %trackingState = fread(fid,1,'uint32');
            if versionRead == 1
                liTimeStamp = fread(fid,1 ,'uint64');	
                dwFrameNumber = fread(fid,1,'uint32');	
                vFloorClipPlane = fread(fid,4,'uint32'); 
                %vFloorClipPlane = fread(fid,16); 
            end
            for i = 1:NUI_SKELETON_COUNT
                %disp('01');
                eTrackingState = fread(fid,1,'uint32');	
                if eTrackingState == NUI_SKELETON_TRACKED
                    %disp('02');
                    dwTrackingID = fread(fid,1,'uint32');	
                    dwEnrollmentIndex = fread(fid,1,'uint32');	
                    dwUserIndex = fread(fid,1,'uint32');	
                    Position = fread(fid,4,'float');
                    count1=count1+1;
                     if flag_gait_cycle==0
                     %debugSkeletonLogFP3 = fopen('joint_tracking_test.txt','a+');
                     %fprintf(debugSkeletonLogFP3,'%s %d\n' ,data{2*iii},count);
                     %fclose(debugSkeletonLogFP3);
                     flag_gait_cycle=1;
                     end
                    %fprintf(debugSkeletonLogFP1,'TRACKED\n');
                    for k = 1:20
                        
                        SkeletonPositionsX = fread(fid,1,'float');	
                        SkeletonPositionsY = fread(fid,1,'float');	
                        SkeletonPositionsZ = fread(fid,1,'float');	
                        SkeletonPositionsW = fread(fid,1,'float');
                       
                        %debugSkeletonLogFP1 = fopen(strcat(path,'Joint_',int2str(k),'.txt'),'a+');
                        %fprintf(debugSkeletonLogFP1,' %f, %f, %f, %f\n' ,SkeletonPositionsX, SkeletonPositionsY, SkeletonPositionsZ,SkeletonPositionsW);
						%fclose(debugSkeletonLogFP1);
                        if k==15
                            ankle_left_posX = SkeletonPositionsX;
                        end
                        if k==20
                            ankle_right_posX = SkeletonPositionsX;
                        end
                          
                    end
                      
                        %debugSkeletonLogFP2 = fopen(strcat(path,'diff.txt'),'a+');
                        %fprintf(debugSkeletonLogFP2,' %f\n' ,abs(ankle_left_posX-ankle_right_posX));
						%fclose(debugSkeletonLogFP2);
                    eSkeletonPositionTrackingState = fread(fid,20 ,'uint32');	
                    dwQualityFlags = fread(fid,1,'uint32');	
                elseif eTrackingState == NUI_SKELETON_POSITION_ONLY
                   
                    PositionX = fread(fid,1,'float');	
                    PositionY = fread(fid,1,'float');	
                    PositionZ = fread(fid,1,'float');	
                    PositionW = fread(fid,1,'float');	
                   
                end
                              
            end
           
                              
        end
           
      end
    fclose(fid);
    %fclose(fid_m);
   
         end   
  
     end         
  toc          
end 

