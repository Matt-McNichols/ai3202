#!/usr/bin/python
#   FIXME: matt
#This is the main file for the Bayes network Assignment

# The  option  flags  in  your  program  need  to  be:
# (-g) conditional  probability
# (-j) joint  probability
# (-m)  marginal  probability
# (-p)  to  set  a  prior  for  either  Pollution  or smoking

# x and d are conditionally independent given c
# p and s are conditionally dependent given c


import getopt, sys
from lib_matt import printV
from Bayes_dict import BN_dict





def main():
    BN = BN_dict();
    # set parents and children


    #printV(BN.pollution_dict['prob_dist'],1);
    #printV(BN.smoker_dict['prob_dist'],1);
    #printV(BN.cancer_dict['prob_dist'],1);
    #printV(BN.x_dict['prob_dist'],1);
    #printV(BN.d_dict['prob_dist'],1);

    ## next organize possible inputs
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ("-p"):
            printV(["flag", o],1);
            printV(["args", a],1);
            printV(a[0],1);
            printV(float(a[1:]),1);
            printV("command to set prior",1);
            #setting the prior here works if the Bayes net is already built
            prior_out=BN.setPrior(a[0], float(a[1:]));
            printV(["prior for ",prior_out[0],"is now",prior_out[1]],2);

        elif o in ("-m"):
            printV(["flag", o],1);
            printV(["args", a],1);
            printV(type(a),1);
            printV("command to compute marginal prob",1);
            # FIXME: matt
            # calculate marginal for a
            a_list=BN.get_arg_list(a);
            printV(["marginal list",a_list],2);
            for a_index in a_list:
                if ('~' is not a_index[0]):
                    printV(['Marginal of',a, "is: ",BN.calcMarginal(a[0])],2);
                else:
                    printV(['Marginal of',a, "is: ",(1-BN.calcMarginal(a[1]))],2);
        elif o in ("-g"):
            printV(["flag", o],1);
            printV(["args", a],1);
            printV(type(a),1);
            printV("command to compute conditional prob",1);
            '''you may want to parse a here and pass the left of |
            and right of | as arguments to calcConditional
            '''
            p = a.find("|")
            printV(a[:p],1);
            printV(a[p+1:],1);
            BN.calcConditional(a[:p], a[p+1:]);
        elif o in ("-j"):
            printV(["flag", o],1);
            printV(["args", a],1);
            printV("command to compute joint prob",1)
            printV(["J= ",BN.calcJoint(a)],2);
        else:
            assert False, "unhandled option"

      # ...

if __name__ == "__main__":
    main()
