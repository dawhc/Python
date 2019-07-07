from neural_network import NeuralNetwork
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)
TRAINFILE_NAME = 'mnist_train.csv'
TESTFILE_NAME = 'mnist_test.csv'

def get_trained_network():
    net = NeuralNetwork(learning_rate = 0.15, input_size = 784, hidden_size = 200, output_size = 10)

    # Training
    print('Training...')
    with open(os.path.join(BASE_DIR, TRAINFILE_NAME)) as f:
        data_list = f.readlines()
    cnt = 0
    total = len(data_list)
    ratio_last = ''
    for data_line in data_list:
        cnt += 1
        ratio = '{:.1%}'.format(cnt/total)
        if ratio != ratio_last:
            ratio_last = ratio
            content = '|{:#^' + str(int(cnt*100./total)) +'}|{}'
            print(content.format('', ratio), end = '\r')
        output_target = [0.01 for i in range(10)]
        output_target[eval(data_line[0])] = 0.99
        input_data = np.asfarray(data_line.split(',')[1:]) / 255. * 0.99 + 0.01
        net.train(input_data, output_target)
    print('Training finished!\nTotal: {}'.format(cnt))
    
    # Testing
    print('Testing...')
    with open(os.path.join(BASE_DIR, TESTFILE_NAME)) as f:
        data_list = f.readlines()
    cnt = 0
    cnt_succ = 0
    total = len(data_list)
    for data_line in data_list:
        cnt += 1
        print('Testning...{}/{}'.format(cnt, total), end = '\r')
        target_number = eval(data_line[0])
        input_data = np.asfarray(data_line.split(',')[1:]) / 255. * 0.99 + 0.01
        output_data = net.query(input_data)
        output_number = np.argmax(output_data)
        if target_number == output_number:
            cnt_succ += 1
    
    print('Testing finished!\nTotal: {}\nSuccessful: {}\nSuccessful rate:{:.2%}\n'.format(cnt, cnt_succ, cnt_succ/cnt))
    return net
 