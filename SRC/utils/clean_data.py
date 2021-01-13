import music21 as m21
import pandas as pd 
import numpy as np 
import os

# We create a function to convert midis in each folder to music21.  


def cleaned():

    def midis_to_m21(i):
        midis=[]
        for dirn, _, filenames in os.walk(f"C:\\Users\\estel\\OneDrive\\Documentos\\data.science.TheBridge\\BB\\beet_midis\\{i}_midis"):
            for filename in filenames:
                file = (os.path.join(dirn, filename))
                midi = m21.converter.parse(file)
                midis.append(midi)
        return midis

    def midis_names(i):
        names=[]
        for dirname, _, filenames in os.walk(f"C:\\Users\\estel\\OneDrive\\Documentos\\data.science.TheBridge\\BB\\beet_midis\\{i}_midis"):
            for filename in filenames:
                names.append(filename.replace(".mid", ""))
        return names



    #we create a variable for each composition category (canons, chamber_music.. ---> canons_m21, chamber_music_m21), aluding to it being a list of m21 objects.
    

    canons_m21=midis_to_m21("canons")
    canons_names=midis_names("canons")

    chamber_music_m21= midis_to_m21("chamber_music")
    chamber_music_names= midis_names("chamber_music")

    concertos_m21=midis_to_m21("concertos")
    concertos_names=midis_names("concertos")

    dances_for_piano_m21=midis_to_m21("dances_for_piano")
    dances_for_piano_names=midis_names("dances_for_piano")

    piano_works_m21=midis_to_m21("piano_works")
    piano_works_names=midis_names("piano_works")

    sonatas_m21=midis_to_m21("sonatas")
    sonatas_names=midis_names("sonatas")

    lied_m21=midis_to_m21("lied")
    lied_names=midis_names("lied")

    symphonies_m21=midis_to_m21("symphonies")
    symphonies_names=midis_names("symphonies")


    piano_variations_m21=midis_to_m21("piano_variations")
    piano_variations_names=midis_names("piano_variations")


    keyboard_other_m21=midis_to_m21("keyboard_other")
    keyboard_other_names=midis_names("keyboard_other")

    dances_orchestra_m21=midis_to_m21("dances_orchestra")
    dances_orchestra_names=midis_names("dances_orchestra")


    orchestra_other_m21=midis_to_m21("orchestra_other")
    orchestra_other_names=midis_names("orchestra_other")


    piano_four_hands_m21=midis_to_m21("piano_four_hands")
    piano_four_hands_names=midis_names("piano_four_hands")

    piano_reduction_m21=midis_to_m21("piano_reduction")
    piano_reduction_names=midis_names("piano_reduction")

    stage_music_m21=midis_to_m21("stage_music")
    stage_music_names=midis_names("stage_music")


    def key_value(m21_variable): 
        keys=[]
        for i in m21_variable:
            keys.append(i.analyze("key"))
        return keys


    #key sig values

    def keySig_value(m21_variable):
        keySig=[]
        for i in m21_variable:
            kS=i.flat.keySignature
            if kS==None:
                kS=m21.key.Key("C")  
            keySig.append(kS)
            
        return keySig

    #first and last chords
    def first_last_chords(m21_variable):
        first_last_chords=[]
        for j in m21_variable:
            f=[]
            l=[]
            
            for i in j.flat.notes[:3]:  #j= a steam for a workpiece in sonatas_m21 for example. flat.notes gets all notes from all parts of the stream in temporal order. [:3]=first 3
                if isinstance(i,m21.note.Note): #as we can have notes or chords in flat.notes we append the notes pitch 
                    f.append(i.pitch)
                if isinstance(i,m21.chord.Chord): #or the notes in the chords pitches one by one. (no pitch for chord)
                    for q in i:
                        f.append(q.pitch)

            for k in j.flat.notes[-3:]: #same for last 3 notes
                if isinstance(k,m21.note.Note):
                    l.append(k.pitch)
                if isinstance(k,m21.chord.Chord):
                    for q in k:
                        l.append(q.pitch)

            cL=m21.chord.Chord(l).closedPosition() #we make a chord out of the last three notes and by closed.Position bring together the chord to the same scale range.
            cF=m21.chord.Chord(f).closedPosition() #cL= last chord, cF= first chord
        
            first_last_chords.append((cF,cL)) #we append them in a tuple 

        return first_last_chords #returns list of tuples for each workpiece, each with the first and last chord


   
    #First and last chord's root:

    def fL_chords_root(m21_variable):
        fLc=first_last_chords(m21_variable) #by calling first_and_last root() 
        fRoot=[]
        lRoot=[]
        for i in range(len(fLc)):
            fRoot.append(fLc[i][0].root().name) 
            lRoot.append(fLc[i][1].root().name)
        return fRoot, lRoot #return a list with 2 lists: one with all first chords root another with last. No tuple format for each workpiece here. 


        #Dataframe 
    def key_dF(m21variable):

        Mm_relatives=[]
        for i in keySig_value(m21variable):
            if i.mode=="major":
                Mm_relatives.append((i,i.relative))
            elif i.mode=="minor":
                Mm_relatives.append((i.relative,i))

        Mm_relatives_Tonics=[]
        for i in Mm_relatives:
            Mm_relatives_Tonics.append((i[0].tonic.name,i[1].tonic.name))
        
        roots=fL_chords_root(m21variable)

        kS_MmF=[]
        kS_MmL=[]
        
        for p,v in enumerate(Mm_relatives):
            if v[0].tonic.name==roots[0][p]:
                kS_MmF.append(v[0])
            elif v[1].tonic.name==roots[0][p]:
                kS_MmF.append(v[1])
            else:
                kS_MmF.append(None)
        
            if v[0].tonic.name==roots[1][p]:
                kS_MmL.append(v[0])
            elif v[1].tonic.name==roots[1][p]:
            
                kS_MmL.append(v[1])
            else:
                kS_MmL.append(None)


        k=key_value(m21variable)
        kT= [i.tonic.name for i in k]
        kS= keySig_value(m21variable)
        ksT= [i.tonic.name for i in kS]
        kn=[i.name for i in k]    #getting the key name 

        kS_d={}

        K=["key.Key","Key","Tonic", "Key Signature","Tonic", "Key Signatures", "Tonics", "First Chord's Root", "Key Deduced 1", "Last Chord's Root", "Key Deduced 2"]
        vals=[k,kn, kT,kS, ksT, Mm_relatives, Mm_relatives_Tonics, roots[0], kS_MmF, roots[1], kS_MmL]

        for i in range(len(K)):
            kS_d[K[i]]=vals[i]
            
        kS_df=pd.DataFrame({key:pd.Series(values) for key, values in kS_d.items()})

        return kS_df


    
    #visualizing key sig analysis for all works by work category Dataframe:
    def keyAnalysis_dfAll(v1,v2):#v1=workpiece_m21 list, v2= first index to differenciate rows by composition category.
        df= pd.concat([key_dF(i) for i in v1], keys= v2) #concatenating dataframes made for each m21 variable in v1
        return df

    #df with names of each work

    def names_df(v_names):
        df_names= pd.concat([pd.DataFrame({"Name":i}) for i in v_names], keys= v2)  #making a dataframe with a list of names of each workpiece   
        return df_names

    #final df

    def final_df(v1,v2,v3):
        df1= names_df(v3)
        df2=keyAnalysis_dfAll(v1,v2)
        final_df= pd.concat([df1,df2], axis= 1)
        return final_df


    #Dtaframe variable saved as dFfinal.
    # v1: all works by composition category as music21 objects. 
    # v2: first index.
    # v3: all work names

    v1=[canons_m21, chamber_music_m21, concertos_m21, dances_for_piano_m21, lied_m21, piano_works_m21, sonatas_m21,piano_four_hands_m21,piano_reduction_m21,piano_variations_m21,keyboard_other_m21,dances_orchestra_m21,orchestra_other_m21,stage_music_m21,symphonies_m21]

    v2= ["canons", "chamber \n music", "concertos", "dances \n piano", "lied", "piano \n works", "sonatas","piano \n 4hands", "piano \n reductions","piano \n variations", "keyboard \n other", "dances \n orchestra", "orchestra \n other", "stage \n music","symphonies"]

    v_names=[canons_names, chamber_music_names, concertos_names, dances_for_piano_names, lied_names, piano_works_names, sonatas_names,piano_four_hands_names,piano_reduction_names,piano_variations_names,keyboard_other_names,dances_orchestra_names,orchestra_other_names,stage_music_names,symphonies_names]


    dFfinal=final_df(v1,v2,v_names)

    return dFfinal


    




