echo ******Hello World from AWS EC2 Instance*******
echo $(hostname -i)

#pip3 install numpy
sudo python3 /home/ubuntu/MLOps/dataproc_gen_data/create_data.py -c 500 -t 100 -d 2 -date 2018-04-20 -r 5