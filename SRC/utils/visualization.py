
import music21 as m21
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns



#function that lists all the names of the composition categories as indexed in the dataframe
def compsF(df):
    comps=[]
    for i in df.index.get_level_values(0): 
        if i not in comps:
            comps.append(i)
    return comps



#Number of keys that can be determined by key sig and first or last chords

def deducible_keys(df):
    
    comps=compsF(df)
        
    perc1=[] 
    perc2=[]
    for i in comps:
        c=df.xs(i)  
        p1=c[["Key Deduced 1"]]
        p2=c[["Key Deduced 2"]]
        perc1.append(len(p1.dropna())/len(p1)*100) #percentage of non None values in key deduced by fist chord and by last. 
        perc2.append(len(p2.dropna())/len(p2)*100)

    #plot
    plt.subplots(figsize=(14, 3))
    plt.ylabel("Percentage")
    plt.title("Key Signature's Tonic equal to First/Last Chord's Root \n \"Deducible Keys\"")

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=comps, y = perc1,label= "First Chord")
    sns.lineplot(x=comps, y = perc2, label= "Last Chord")
    
    plt.legend() #show labels
    
    return plt.show()
    


def deducible_keys_barplot(df):
    comps=compsF(df)
    
    perc1=[] #percentage of key deduced 1 not None
    perc2=[]  #percentage of key deduced 2 not none 
    perc3=[]  #percentage of key decuded 1 = key deduced 2
    for i in comps:
        c=df.xs(i)  
        d1=len(c["Key Deduced 1"].dropna())     #numer of not none values= number of deduced keys
        d2=len(c["Key Deduced 2"].dropna())
        d3=c["Key Deduced 1"]== c["Key Deduced 2"] #series of true false values none==none is False.
        perc1.append(d1/len(c["Key Deduced 1"])*100) 
        perc2.append(d2/len(c["Key Deduced 2"])*100)
        perc3.append(list(d3).count(True)/ len(d3)*100) #number of true values in the series made percentage, (key decuded 1 = key deduced 2)
        

    x = np.arange(len(comps)) #x labels
    width = 0.35 #width of bars

    #multibar plots
    plt.subplots(figsize=(15, 5))
    plt.grid(True)
    plt.bar(x - width/2, perc1, width, label="By First Chord") #by first chord
    p2=plt.bar(x + width/2, perc2, width, label="By Last Chord",color="purple", alpha= 0.7) #by last chord (bars next to first bars)

    #plot labels
    plt.ylabel('Percentage')
    plt.title("Deduced Key Signature's by First/Last Chord's Root", size=15)
    plt.xticks(x,comps)
    plt.legend()
    plt.xlabel("The mark on second bars indicate the percentage of keys deduced by first chord which are also deduced by the last chord.", size= 10)
    #making a mark on second bars to indicate the percentage of keys deduced by first chord which are also deduced by the last chord. 
    
    for i,p in enumerate(p2):
        height = perc3[i]
        plt.annotate('{}'.format("****"),
                xy=(p.get_x() + p.get_width() / 2, height),
                xytext=(0, -3),
                textcoords="offset points",
                size=6,
                ha='center', va='bottom')
    
    return plt.show()



#key equals key signature (deduced by fist chord if not second if not given by default)
def key_eq_keySig(df):
    comps=compsF(df)
    perc=[]
    for i in comps:
        c=df.xs(i)
        k=[]
        for j in range(len(c["key.Key"])):
            if c["Key Deduced 1"][j] != None:  
                k.append(c["key.Key"][j]==c["Key Deduced 1"][j])   #append whether the key density is equal to the key deduced by the first chord.
            else: 
                k.append(c["key.Key"][j]==c["Key Signature"][j] or c["key.Key"][j]==c["Key Signature"][j].relative)     #if no key counld be deduced append whether it is equal to the key signature or its relative
            
        perc.append(k.count(True)/len(k)*100)
    

    plt.subplots(figsize=(15, 4))
    plt.ylabel("Percentage")
    plt.title("Key equals Key Signature")

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=comps, y = perc)
    
    return plt.show()



def k_kS_ded(df):
    comps=compsF(df)
    perc=[]
    for i in comps:
        c=df.xs(i)
        k=[]
        for j in range(len(c["key.Key"])):
            if c["Key Deduced 1"][j] != None:
                k.append(c["key.Key"][j]==c["Key Deduced 1"][j])
            else: 
                k.append(c["key.Key"][j]==c["Key Signature"][j] or c["key.Key"][j]==c["Key Signature"][j].relative)
            
        perc.append(list(k).count(True)/len(k)*100)
    
    perc1=[]
    perc2=[]
    for i in comps:
        c=df.xs(i)  
        p1=c[["Key Deduced 1"]]
        p2=c[["Key Deduced 2"]]
        perc1.append(len(p1.dropna())/len(p1)*100)
        perc2.append(len(p2.dropna())/len(p2)*100)

    plt.subplots(figsize=(14, 3))
    plt.ylabel("Percentage")
    plt.title("Deduced Keys by First/Last Chord \n and music21 default Key (density key) equal to Deduced Keys")

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=comps, y = perc1,label= "First Chord")
    sns.lineplot(x=comps, y = perc2, label= "Last Chord")
    
    plt.legend()
    

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=comps, y = perc, label="Density Key")

    return plt.show()

#barplot deduced by first, key density, deduced by last
def keys_fDs_barplot(df):
    comps=[]
    for i in df.index.get_level_values(0): #get the names of the composition categories as in the dataframe.
        if i not in comps:
            comps.append(i)
    perc=[]
    for i in comps:
        c=df.xs(i)
        k=[]
        for j in range(len(c["key.Key"])):
            if c["Key Deduced 1"][j] != None:  
                k.append(c["key.Key"][j]==c["Key Deduced 1"][j])
            else: 
                k.append(c["key.Key"][j]==c["Key Signature"][j] or c["key.Key"][j]==c["Key Signature"][j].relative)
            
        perc.append(list(k).count(True)/len(k)*100)
    
    perc1=[]
    perc2=[]
    for i in comps:
        c=df.xs(i)  
        p1=c[["Key Deduced 1"]]
        p2=c[["Key Deduced 2"]]
        perc1.append(len(p1.dropna())/len(p1)*100)
        perc2.append(len(p2.dropna())/len(p2)*100)

    #multibarplot
    x = np.arange(len(comps)) #x labels
    width = 0.3 #width of bars

    plt.subplots(figsize=(15, 4))
    plt.bar(x - width, perc1, width, label="By First Chord") #by first chord
    plt.bar(x, perc, width, label="Key Density", color= "gray", alpha=0.7) #overall (key density)
    plt.bar(x + width, perc2, width, label="By Last Chord",color="purple",alpha=0.9) #by last chord
    
    #labels
    plt.ylabel("Percentage")
    plt.title("Deduced Keys by First/Last Chord \n and music21 default Key (density key) equal to Deduced Keys")
    plt.xticks(x,comps)
    plt.legend()
    plt.grid(False)
    
    return plt.show()

def key_eq_Ded1(df):
    comps=compsF(df)
    perc1=[]
    perc2=[]
    for i in comps:
        c=df.xs(i)
        k1=[]
        k2=[]
        for j in range(len(c["key.Key"])):
            if c["Key Deduced 1"][j] != None:
                k1.append(c["key.Key"][j]==c["Key Deduced 1"][j])
            else:
                k2.append(c["key.Key"][j]==c["Key Signature"][j]  or c["key.Key"][j]==c["Key Signature"][j].relative)
            
        perc1.append(list(k1).count(True)/len(k1)*100)
        try:
            perc2.append(list(k2).count(True)/len(k2)*100)
        except:
            perc2.append(0)
 
    
    plt.subplots(figsize=(15, 4))
    plt.ylabel("Percentage")
    plt.title("Key Density equals Key Deduced by First Chord vs Undeduced")

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=comps, y = perc1, label= "Deduced")
    sns.lineplot(x=comps,y= perc2, label= "Undeduced")
    plt.legend()

  
    return plt.show()



#first and second most used keys per composition category:
 
def key_first_sec(df):
    comps=compsF(df)
    b=[]
    y=[]
    ran= []
    median_perc=[]

    for i in comps:
        dkc=df.xs(i).groupby("Key").count() #all columns will contain the same count values 

        b.append(dkc.nlargest(2,"Tonic").index) #we choose keySig to obtain the counts although they are not related to the column name keysig.  

        y.append([dkc.nlargest(2,"Tonic").iloc[:,0][i]/dkc["Key Signature"].sum()*100 for i in range(2)])
    
        median_perc.append(dkc["Key Signature"].median()/dkc["Tonic"].sum()*100)

        ran.append(len(dkc["Key Signature"]))

    y1=[i[0] for i in y]
    y2=[i[1] for i in y]

    b1=[i[0] for i in b]
    b2=[i[1] for i in b]

    x = np.arange(len(b))  # the label locations
    width = 0.35  # the width of the bars

    plt.subplots(figsize=(15,5))
    p1=plt.bar(x - width/2, y1, width, label='Most used key')
    p2=plt.bar(x + width/2, y2, width, label='Second most used',color="purple", alpha= 0.7)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Percentage')
    plt.title("Most Used Key's per Composition Category")
    plt.xticks(x,comps)
    plt.legend()
    plt.xlabel("Number of keys used per category shown at the bottom of first bars. \n Median percentage shown by mark in first bars.", size=7, ha="left")


    #labeling the bars
    for i,p in enumerate(p1):
        height = p.get_height()
        plt.annotate('{}'.format(b1[i]),
                xy=(p.get_x() + p.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                size=6,
                ha='center', va='bottom')

    for i,p in enumerate(p2):
        height = p.get_height()
        plt.annotate('{}'.format(b2[i]),
                xy=(p.get_x() + p.get_width() / 4, height),
                xytext=(0,3),  # 3 points vertical offset
                textcoords="offset points",
                size=6,
                ha='left', va='bottom')
    #median percentage
    for i,p in enumerate(p1):
        height = median_perc[i]
        plt.annotate('{}'.format("****"),
                xy=(p.get_x() + p.get_width() / 2, height),
                xytext=(0, -3),  # 3 points vertical offset
                textcoords="offset points",
                size=6,
                ha='center', va='bottom')
    #number of keys used
    for i,p in enumerate(p1):
        height = 0.5
        plt.annotate('{}'.format(ran[i]),
                xy=(p.get_x() + p.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                size=6,
                ha='center', va='bottom')
    plt.grid(True)

    return plt.show()


#Rare Keys = Keys with 6 or more sharps or flats: sharps= positive int, flats= negative int. 
def rare_keys():
    all_keys=[]
    all_keys_names=[]

    all_k=["A","a","B","b","C","c","D","d", "E", "e", "F", "f", "G", "g","A-","B-","b-","C#","c#", "E-", "e-", "F#", "f#", "g#"] #all key names 
    for i in all_k:
        all_keys.append(m21.key.Key(i)) #convert to keys 
    for i in all_keys:
        all_keys_names.append(i.name) #get full name

    sharps_flats=[]
    for i in all_keys:
        sharps_flats.append(i.sharps) #get sharps/flats from key object.
    dsf={}
    for i in range(len(all_keys_names)):   #make dictionary keys= key names, values= number of sharps/flats
        dsf[all_keys_names[i]]=sharps_flats[i]

    rare_keys=[i for i in dsf.keys() if dsf[i]>=6 or dsf[i]<=-6] #list keys whose values have a magnitude of 6 or above.
    return rare_keys

#getting the "rare key" works and their names along with their composition category.
def rareK_works(df):
    comps=compsF(df)
    w=[]
    for i in comps:
        c=df.xs(i)
        for j in range(len(c["Key"])):
            if c["Key"][j] in rare_keys():
                w.append((c["Key"][j],c["Name"][j], i))
    return w

#Number of works per tonality 

def key_counts(df):
    
    a=df.groupby("Key").count()["Tonic"].sort_values(ascending= True).index  #all keys listed by ascending order due to counts.
    b= list(df.groupby("Key").count()["Tonic"].sort_values(ascending= True))  #list of counts per key 
    
    col=[]    
    for p,v in enumerate(a):   #podition of rare keys (with more than 5 sharps or flats) 
        if v in rare_keys():
            col.append(p)

    plt.subplots(figsize=(10,5))
    p1= plt.barh(a,b)
    plt.title("Number of Works per Tonality")

    for i in col:
        p1[i].set_color("purple") #color the bars of the rare keys

    plt.grid(True)

   
    return plt.show()

#obtaining graph with works with more than 6 sharps or flats(names, keys, comp cat)
def rareKw_plot(df):
    comps=compsF(df)
    w=[]
    for i in comps:
        c=df.xs(i)
        for j in range(len(c["Key"])):
            if c["Key"][j] in rare_keys():
                w.append((c["Key"][j],c["Name"][j], i)) #listing tuple with (rareKey, work name, comp category) for each rare key
    
    x=[i[-1] for i in w] #listing comp category
    y =[i[0] for i in w] #rare key
    z=[i[1]for i in w] #works name

    rare_df=pd.DataFrame({"Composition Category": pd.Series(x), "Keys": pd.Series(y), "Names": pd.Series(z)}) #dataframe

    #plot
    plt.subplots(figsize=(9,4))
    plt.title("Works in Key with more than 5 Sharps or Flats")
    sns.set_style("white")
    sns.stripplot(x="Composition Category", y="Keys", data=rare_df, hue="Names", jitter=True)
    
    return plt.show()




#obtaining the percentage of works in major key per composition category from our dataframe:

def major_works(df):
    comps=compsF(df)
    m=[]

    for i in comps:
        data=df.xs(i)
        c=0
        for j in data["Key"]:
            if "major" in j:
                c+=1
        m.append(c/len(data["Key"])*100)

    x=comps
    y=m

    plt.subplots(figsize=(15, 4))
    plt.plot(x,y)
    plt.yticks(range(60,105,5))
    plt.xticks(size= 8)
    plt.title("Percentage of Works in Major Key")
    plt.grid(True)
  
    return plt.show()

#obtaining the percentage of works in major key per composition category from our dataframe:

def major_works_keyDed(df):
    comps=[]
    for i in df.index.get_level_values(0): #get the names of the composition categories as in the dataframe.
        if i not in comps:
            comps.append(i)
    m=[]

    for i in comps:
        c=df.xs(i)
        count=0
        for j in range(len(c["key.Key"])):     #counting major keys (keys being specified by those deduced by the first chord, else by the one given by default (density key).)
            if c["Key Deduced 1"][j] != None:  
                if c["Key Deduced 1"][j].mode =="major":
                    count+=1
            else:
                if "major" in c["Key"]:
                    count+=1

        
        m.append(count/len(c["Key"])*100)

    x=comps
    y=m

    plt.subplots(figsize=(15, 4))
    plt.plot(x,y)
    plt.yticks(range(40,105,5))
    plt.xticks(size= 8)
    plt.title("Percentage of Works in Major Key \n Deduced Key if not Default")
    plt.grid(True)
   
    return plt.show()


#pie chart

def my_pie():
    done=["Music Theory", "Music21", "Data Search", "Data Colect/Clean", "Undersatand Data for Hypothesis", "Defining Plots", "Putting it all together."]
    time=[20, 20, 5, 5, 20,15,10]
    plt.subplots()  
    plt.pie(time, labels= done)
    plt.title("Aproximate Percentage of Time Invested \n in each Stage of the Project.")

    return plt.show()


