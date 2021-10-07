# Practical Deep Reinforcement Learning Approach for Stock Trading


## Prerequisites
Python 3.6 envrionment

## Step 1: Install OpenAI Baselines System Packages [OpenAI Instruction](https://github.com/openai/baselines)
### Ubuntu
```bash
sudo apt-get update && sudo apt-get install cmake libopenmpi-dev python3-dev zlib1g-dev
```
### Mac OS X
Installation of system packages on Mac requires [Homebrew](https://brew.sh). With Homebrew installed, run the following:
```bash
brew install cmake openmpi
```


## Step 2: Create and Activate Virtual Environment
Clone this repo and cd into it:
```bash
git clone https://github.com/hust512/DQN-DDPG_Stock_Trading.git
cd DQN-DDPG_Stock_Trading
```
Under this folder DDPG_Stock_Trading, create a virtual environment
```bash
pip install virtualenv
```
Virtualenvs are essentially folders that have copies of python executable and all python packages.
To create a virtualenv called venv with python3, one runs
```bash
virtualenv -p python3 venv
```
To activate a virtualenv:
```
source venv/bin/activate
```
Your terminate bash will become something like this:
```
(venv) bruceyang-MBP:DQN-DDPG_Stock_Trading bruce$
```

## Step 3: Install openAI gym environment under this virtual environment: venv
#### Tensorflow versions
The master branch supports Tensorflow from version 1.4 to 1.14. For Tensorflow 2.0 support, please use tf2 branch. Refer to [TensorFlow installation guide](https://www.tensorflow.org/install/)
for more details.
- Install gym and tensorflow packages:
    ```bash
    pip install gym
    pip install gym[atari] 
    pip install tensorflow==1.14
    ```
- Other packages that might be missing:
    ```bash
    pip install filelock
    pip install matplotlib
    pip install pandas
    ```
## Step 4: Download and Install Official Baseline Package
- Clone the repo and cd into it:
    ```bash
    git clone https://github.com/openai/baselines.git
    cd baselines
    ```

- Install baselines package
    ```bash
    pip install -e .
    ```

## Step 5: Testing the installation
All unit tests in baselines can be run using pytest runner:
```
pip install pytest
pytest
```
All unit tests have to get passed, in the end you will see something like: 94 passed, 49 skipped, 72 warnings in 355.29s. If there are any errors or failed tests, you have to debug it, check the openai baselines [Issues](https://github.com/openai/baselines/issues) or stackoverflow to make sure all unit tests passed in the end.

## Step 6: Test-run the OpenAI Atari Pong
### If this works for you then you are ready to implement the stock trading application
`--save_path` and `--load_path` command-line option loads the tensorflow state from a given path before training, and saves it after the training, respectively.
Let's imagine you'd like to train ppo2 on Atari Pong,  save the model and then later visualize what has it learnt. Set num_timesteps to 1e4 for test-run
```bash
python -m baselines.run --alg=ppo2 --env=PongNoFrameskip-v4 --num_timesteps=1e4 --save_path=~/models/pong_20M_ppo2
```
This should get to the mean reward per episode about 20. To load and visualize the model, we'll do the following - load the model, train it for 0 steps, and then visualize:
```bash
python -m baselines.run --alg=ppo2 --env=PongNoFrameskip-v4 --num_timesteps=0 --load_path=~/models/pong_20M_ppo2 --play
```

## Step 7: Register the Stock Trading Environment under gym

## Replace files with files in this repository and change file address

### gym
Find your gym package under environment folder, in my computer it is under
```bash
/Users/xiongzhuoran/anaconda3/envs/venv/lib/python3.6/site-packages/gym/
```
- Replece the file
```bash
gym\envs\__init__.py
```
with file from this repository
```bash
DQN_Stock_Trading/gym/envs/__init__.py
```

- Add folder in this repository to gym\envs in your computer
```bash
DQN_Stock_Trading/gym/envs/zxstock of this repository
```

- Open
```bash
gym/envs/zxstock/zxstock_env.py and gym/envs/zxstock/zxstock_testenv.py
```
change the address at line 9 and line 10 into where you want to save the image

### Baseline
- Open your baselines folder cloned before, find
```bash
baselines/baselines/run.py
```

- Replace it with
```bash
DQN_Stock_Trading/baselines/baselines/run.py in this reposotory
```

## Training model and Testing
If you only want to train the model run this
```bash
python -m baselines.run --alg=ddpg --env=ZXStock-v0 --network=mlp --num_timesteps=1e4
```

If you also want to see the testing result
```bash
python -m baselines.run --alg=ddpg --env=ZXStock-v0 --network=mlp --num_timesteps=1e4 --play
```



### Some Other Commands May Need:
Tensorflow Update
```bash
pip install --upgrade tensorflow==1.11.0
```
```bash
pip3 install opencv-python
pip3 install lockfile
pip3 install -U numpy
pip3 install mujoco-py==0.5.7
```

#### Please cite the following paper
Xiong, Z., Liu, X.Y., Zhong, S., Yang, H. and Walid, A., 2018. Practical deep reinforcement learning approach for stock trading, NeurIPS 2018 AI in Finance Workshop.
