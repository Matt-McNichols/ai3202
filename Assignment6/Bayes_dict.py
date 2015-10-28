#!/usr/bin/python
import math
from lib_matt import printV

class BN_dict:
    # setup Bayes network
    def __init__ (self):
        self.cpt = {'p':[0.9], 's':[0.3], 'c':[0.05,0.02,0.03,0.001], 'x':[0.9,0.2], 'd':[0.65,0.30]};
        self.parents = {'p':[],'s':[],'c':['p','s'],'x':['c'],'d':['c']};
        self.children = {'p':['c'],'s':['c'],'c':['x','d'], 'x':[], 'd':[]}
        self.prior = {'p':0.9,'s':0.3,'c':None};
        self.marginal={'p':0.9, 's':0.3, 'c':None, 'x':None, 'd':None};

    # ...



    def calcMarginal(self,key):
        if (key == 'p')is True or (key == 's')is True:
            return self.marginal[key];
        # update_pi with no evidence is same as marginal

        parent = self.parents[key];
        key_cpt = self.cpt[key];

        printV(["inside calcMarginal key: ",key],1);
        printV(["key_cpt:",key_cpt[0]],1);

        # recursinve call update_pi for parents
        for index_parent in parent:
            self.calcMarginal(index_parent);



#       FIXME: matt
#       change this to work for any node with two parents

        if (key == 'c')is True:
            self.marginal[key] = (
                              (1-self.marginal[parent[0]])  *
                              (self.marginal[parent[1]])    *
                              (key_cpt[0])            +

                              (1-self.marginal[parent[0]])  *
                              (1-self.marginal[parent[1]])  *
                              (key_cpt[1])            +

                              (self.marginal[parent[0]])    *
                              (self.marginal[parent[1]])    *
                              (key_cpt[2])            +

                              (self.marginal[parent[0]])    *
                              (1-self.marginal[parent[1]])  *
                              (key_cpt[3])
                          );
            printV(self.marginal[key],1);
            return self.marginal[key];
        else :
            self.marginal[key] = (
                              (self.marginal[parent[0]])    *
                              (key_cpt[0])            +

                              (1-self.marginal[parent[0]])   *
                              (key_cpt[1])
                           );
            printV(self.marginal[key],1);
            return self.marginal[key];





    def calcJoint(self,key_list):
        arg_list=self.get_arg_list(key_list);
        printV(["arg_list: ",arg_list],1);
        joint = 1;
        for arg in arg_list:
            printV(["arg: ",arg[0]],1);
            if('~' is not arg[0]):
                self.calcMarginal(arg[0]);
                joint = joint * self.marginal[arg[0]];
            else:
                # case when there is ~
                self.calcMarginal(arg[1]);
                joint = joint * (1-self.marginal[arg[1]]);
        return joint;




    # in: key_list --> out arg_list
    def get_arg_list(self,key_list):
        index=-1;
        arg_list = [];
        temp_key_list=list(reversed(key_list));
        while (temp_key_list):
            #index = index + 1;
            temp_key=temp_key_list.pop();
            #printV(key_list[index],0);
            if (temp_key == '~')is True:
                next_key=temp_key_list.pop();
                temp = temp_key+next_key;
                arg_list.append(temp);
            else: arg_list.append(temp_key);
        return arg_list;






    def setPrior(self,key,value):
        if (key == 'P')is True:
            self.marginal['p'] = value;
            self.prior['p'] = value;
            return ['p',self.marginal['p']];
        elif(key == 'S')is True:
            self.marginal['s'] = value;
            self.prior['s'] = value;
            return ['s',value];
        else:
            printV("ERROR: cant set prior to given key");






    # calculate marginal of E list
    def marg_E(self,E_list):
        E_list=self.get_arg_list(E_list);
        for E in E_list:
            if '~' is not E[0]:
                self.calcMarginal(E[0]);
            else: self.calcMarginal(E[1]);

    # return 1 if all evidence is above key
    # return 0 else
    def isCausal(self,key,E_list):
        E_list=self.get_arg_list(E_list);
        r_val = 1;
        # recursive check
        for ch_key in self.children[key]:
            self.isCausal(ch_key,self.children[ch_key]);

        for E in E_list:
            if '~' is not E[0]:
                for ch_key in self.children[key]:
                    if E[0] is ch_key:
                        printV(["found evidence",E[0],"is not a parent of",key],1);
                        r_val=0;
            else:
                for ch_key in self.children[key]:
                    if E[1] is ch_key:
                        printV(["found evidence",E[1],"is not a parent of",key],1);
                        r_val=0;
        return r_val;


    # return 1 if all evidence is below key
    # return 0 else
    def isDiagnostic(self,key,E_list):
        E_list=self.get_arg_list(E_list);
        r_val = 1;

        # recursive check
        for ch_key in self.children[key]:
            self.isDiagnostic(ch_key,self.children[ch_key]);

        for E in E_list:
            if '~' is not E[0]:
                for p_key in self.parents[key]:
                    if E[0] is p_key:
                        printV(["found evidence",E[0],"is not a child of",key],1);
                        r_val=0;
            else:
                for p_key in self.parents[key]:
                    if E[1] is p_key:
                        printV(["found evidence",E[1],"is not a child of",key],1);
                        r_val=0;
        return r_val;


    # only call for E with children
    def prior_given_E(self,E_list):
        E_list=self.get_arg_list(E_list);
        for E in E_list:
            if '~' is not E[0]:
                self.prior[E[0]] = 1;
            else: self.prior[E[1]] = 0;


    def calcProb_given_E(self,key):
        if (key == 'p')is True or (key == 's')is True:
            return self.prior[key];
        # update_pi with no evidence is same as marginal

        parent = self.parents[key];
        key_cpt = self.cpt[key];

        printV(["inside calcMarginal key: ",key],1);
        printV(["key_cpt:",key_cpt[0]],1);

        for index_parent in parent:
            self.calcProb_given_E(index_parent);



#       FIXME: matt
#       change this to work for any node with two parents

        # p --> pollution = low
        # given p, prior(p)--> 1
        # if prior[parent]_0 (pollution) = 0 then pollution = h
        if (key == 'c')is True:
            self.prior[key] = (
                              (1-self.prior[parent[0]])  *
                              (self.prior[parent[1]])    *
                              (key_cpt[0])            +

                              (1-self.prior[parent[0]])  *
                              (1-self.prior[parent[1]])  *
                              (key_cpt[1])            +

                              (self.prior[parent[0]])    *
                              (self.prior[parent[1]])    *
                              (key_cpt[2])            +

                              (self.prior[parent[0]])    *
                              (1-self.prior[parent[1]])  *
                              (key_cpt[3])
                          );
            printV(self.prior[key],1);
            return self.prior[key];
        else :
            self.prior[key] = (
                              (self.prior[parent[0]])    *
                              (key_cpt[0])            +

                              (1-self.prior[parent[0]])   *
                              (key_cpt[1])
                           );
            printV(self.prior[key],1);
            return self.prior[key];



    def calcConditional(self,key,E_list):
        E_list=self.get_arg_list(E_list);
        printV("in calcConditional",1);
        printV(["key: ",key," evidence: ",E_list],1);
        #compute marginal for key and all E nodes
        self.calcMarginal(key);
        self.marg_E(E_list);

        #check if the evidence is causal
        if (self.isCausal(key,E_list) == 1):
            printV("the evidence is purely causal",1);
            # set priors according to evidence
            self.prior_given_E(E_list);
            return_val = self.calcProb_given_E(key)
            printV(["probability of", key,"given",E_list,"is:",return_val],2);
            return return_val;


        #check if the evidence is diagnostic
        if (self.isDiagnostic(key,E_list) == 1):
            printV("the evidence is purely diagnostic",1);
            # use bayes to calculate by finding causal conditionals and marginals
            # only works for 1 evidence
            for E in E_list:
                if '~' is not E[0]:
                    cond_flip = self.calcConditional(E[0],key);
                    return_val= ((cond_flip * self.marginal[key])/self.marginal[E[0]]);
                    printV(["probability of", key,"given",E_list,"is:",return_val],2);
                    return return_val;
                else:
                    cond_flip = (1 - self.calcConditional(E[1],key));
                    return_val ((cond_flip * self.marginal[key])/self.marginal[E[1]]);
                    printV(["probability of", key,"given",E_list,"is:",return_val],2);
                    return return_val;
