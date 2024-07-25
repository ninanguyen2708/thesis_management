# class for thesis topics: 
class Topic:
    # default desList to empty if not provided
    def __init__(self, id, loc, dep, supervisor, title, category, des, desList=None):
        self.id = id   # 1: topic number
        self.loc = loc
        self.dep = dep
        self.supervisor = supervisor # 2: supervisor
        self.title = title # 3: title
        self.category = category  #4: category
        self.des = des # 5: description
        self.desList = desList # 6: create this list for the bullet points in the description of the topic number 41
        if desList is None:
            desList = []
            
class Member:
    def __init__(self, name, nick, id, course):
        self.name = name
        self.nick = nick
        self.id = id
        self.course = course

thesisList = [
    # 'classess.*' -> use class with name * from 'classes.py'
    # Example: Topic -> class with name 'Topic' from classes.py
    Topic(1, #1 
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Computer Science', 'Information Systems', 'Software Engineering'],
            'Bharanidharan Shanmugam', #2
            'Machine learning approaches for Cyber Security',#3
            ['Artificial Intelligence', 'Machine Learning', 'Data Science'],#4
            'As we use internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.'
        ),
    Topic(9, 
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Computer Science', 'Cyber Security', 'Data Science', 'Information Systems and Data Science', 'Software Engineering'],
            'Yakub Sebastian',
            'Informetrics applications in multidisciplinary domain',
            ['Artificial Intelligence', 'Machine Learning', 'Data Science'],
            'Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science and bibliometric techniques on various information artefact have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualisation and data wrangling tools.'
        ),  
    Topic(16,
            ['Internal - Casuarina', 'External'],
            ['Electrical and Electronics Engineernig', 'Computer Science', 'Software Engineering'],
            'Sami Azam',
            'Development of a Virtual Reality System to Test Binaural Hearing',
            ['Biomedical Engineering', 'Health Informatics'],
            'A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off the shelf components (VR goggle and headphones) and standard programming techniques.'
        ),
    Topic(41, #1
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Computer Science', 'Cyber Security', 'Software Engineering'],
            'Sami Azam', #2
            'Current trends on cryptomining and its potential impact on cryptocurrencies', #3
            ['Cyber Security'], #4
            "Cryptomining is the process of mining crypto currencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. Some website owners have started taking a different approach; they have put the software which runs those difficult calculations into their website's Javascript. This then causes the computers belonging to the visitors of their website to run those calculations for them, instead of running them themselves. In other words, when you visit a website with an embedded crypto-miner in it, your computer and electricity is used to try to generate crypto-coins for the owners of that website. Although there are various measures being applied to stop these illegitimate minings, the trend is still increasing. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out:", #5
            ['What type crypto mining methodologies are being applied?', 'Apart from crypto-mining, what other security risks may it introduce? For example: cryptojacking', 'How current web standards are tackling this problem?'] #6
        ),
    Topic(176,
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Electrical and Electronics Engineernig', 'Computer Science', 'Data Science', 'Software Engineering'],
            'Asif Karim',
            'Artificial Intelligence in Health Informatics',
            ['Artificial Intelligence', 'Machine Learning', 'Data Science'],
            'The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.'
        ),
    Topic(180,
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Electrical and Electronics Engineernig', 'Computer Science', 'Data Science', 'Software Engineering'],
            'Asif Karim',
            'Unsupervised Model Development from Autism Screening Data',
            ['Artificial Intelligence', 'Machine Learning', 'Data Science'],
            'The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.'
        ),
    Topic(226, 
            ['Internal - Casuarina', 'Internal - Sydney', 'External'],
            ['Chemical Engineering', 'Civil and Structural Engineering', 'Electrical and Electronics Engineernig', 'Mechanical Engineering', 'Computer Science', 'Cyber Security', 'Data Science', 'Information Systems and Data Science', 'Software Engineering'],
            'Bharanidharan Shanmugam', 
            'Applying Artificial Intelligence to solve real world problems',
            ['Artificial Intelligence', 'Machine Learning', 'Data Science'],
            'Artificial Intelligence has been used in many applications to solve certain problems through out the academia and the industry – from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include -building a bot, predicting the power usage, spam filtering and the list is endless.'
        )
]

mem = [
    Member('Le Phuong Khanh Nguyen', 'Nina', 371506, 'Bachelor of Information Technology'),
    Member('Vinh Kien Tran', 'Ken', 367251, 'Bachelor of Information Technology'),
    Member('Keagen Leon Smith', '', 370836, 'Bachelor of Information Technology'),
    Member('Huy Hieu Ha', 'Harry', 368697, 'Bachelor of Information Technology')
]

loc = ['Internal - Casuarina', 'Internal - Sydney', 'External']
dep = ['Chemical Engineering', 'Civil and Structural Engineering', 'Electrical and Electronics Engineernig', 'Mechanical Engineering', 'Computer Science', 'Cyber Security', 'Data Science', 'Information Systems and Data Science', 'Software Engineering']
cat = ['Artificial Intelligence', 'Machine Learning', 'Data Science', 'Biomedical Engineering', 'Health Informatics', 'Cyber Security']
sup = ['Bharanidharan Shanmugam', 'Yakub Sebastian', 'Sami Azam', 'Asif Karim']
