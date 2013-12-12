filename = 'linearInterp.txt';
figure(1)
LinearInterp = csvread(filename,0,0);
plot(LinearInterp(1,:),LinearInterp(2,:),'-*')
% title('Language model with Linear Interpolation smoothing')
xlabel('lambda')
ylabel('Mean Average Precision (MAP)')

filename = 'dirichlet.txt';;
figure(2)
Dirichlet = csvread(filename,0,0);
plot(Dirichlet(1,:),Dirichlet(2,:),'-*')
% title('Language model with Dirichlet smoothing')
xlabel('alpha')
ylabel('Mean Average Precision (MAP)')

 Xbm=[0,0.25,0.5,0.75,1;0,0.25,0.5,0.75,1;0,0.25,0.5,0.75,1;0,0.25,0.5,0.75,1;0,0.25,0.5,0.75,1];
 Ybm=[0.0,1.2,2.4, 3.6,4.8;0.0,1.2,2.4, 3.6,4.8;0.0,1.2,2.4, 3.6,4.8;0.0,1.2,2.4, 3.6,4.8;0.0,1.2,2.4, 3.6,4.8];
 Ybm=Ybm';
 Zbm=[0.6964,0.7263,0.7346,0.7424,0.7450;0.6964,0.7590,0.7636,0.7719,0.7773;0.6964,0.7699,0.7733,0.7790,0.7863;0.6964,0.7680,0.7713,0.7742,0.7787;0.6964,0.7519,0.7560,0.7576,0.7593];
Zbm=Zbm';
figure(4)
surf(Xbm,Ybm,Zbm)
%best for bm25 b=0.5 b=4.8


 x=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0];
yDir=[1,0.8596,0.8596,0.8596,0.8596,0.8596,0.6406,0.5842,0.5732,0.3952,0.1839];
yLinear=[1,1,0.9286,0.9286,0.9146,0.9022,0.6591,0.6521,0.6289,0.5809,0.1839];
yTfidf=[0.9062,0.9062,0.8788,0.8788,0.8529,0.8491,0.7346,0.6107,0.5982,0.5935,0.2714];
yBM25=[1,1,0.9259,0.9259,0.87,0.87,0.7444,0.6968,0.6565,0.6018,0.2591];
yComb=[1,1,0.9259,0.9259,0.87,0.87,0.7793,0.65,0.6395,0.6172,0.2879];


figure(3)

hlines=plot(x,yDir,'-+',x,yLinear,'-*',x,yTfidf,'-o',x,yBM25,'-s',x,yComb,'--')
set(hlines(1),'Displayname','LangModel Dirichlet')
 set(hlines(2),'Displayname','LangModel Linear Interpolation')
set(hlines(3),'Displayname','TFIDF')
set(hlines(4),'Displayname','BM25')
set(hlines(5),'Displayname','Combined')
legend(hlines);
% title('Precision recall curves for different models')
xlabel('recall')
ylabel('precision')

