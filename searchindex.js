Search.setIndex({docnames:["command_parser.commands","command_parser.config","command_parser.error_handling","command_parser.exceptions","command_parser.formatting","command_parser.nargs","command_parser.parameters","command_parser.parser","command_parser.utils","index"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["command_parser.commands.rst","command_parser.config.rst","command_parser.error_handling.rst","command_parser.exceptions.rst","command_parser.formatting.rst","command_parser.nargs.rst","command_parser.parameters.rst","command_parser.parser.rst","command_parser.utils.rst","index.rst"],objects:{"command_parser.commands":[[0,1,1,"","BaseCommand"],[0,1,1,"","Command"]],"command_parser.commands.BaseCommand":[[0,2,1,"","__init_subclass__"],[0,3,1,"","args"],[0,4,1,"","command_config"],[0,2,1,"","main"],[0,2,1,"","parse"],[0,2,1,"","parse_and_run"],[0,4,1,"","parser"],[0,2,1,"","run"]],"command_parser.commands.Command":[[0,2,1,"","help"],[0,2,1,"","run"]],"command_parser.config":[[1,1,1,"","CommandConfig"]],"command_parser.config.CommandConfig":[[1,3,1,"","action_after_action_flags"],[1,3,1,"","multiple_action_flags"]],"command_parser.error_handling":[[2,1,1,"","ErrorHandler"]],"command_parser.error_handling.ErrorHandler":[[2,2,1,"","cls_handler"],[2,2,1,"","copy"],[2,2,1,"","get_handler"],[2,2,1,"","register"],[2,2,1,"","unregister"]],"command_parser.exceptions":[[3,5,1,"","BadArgument"],[3,5,1,"","BadArgumentUsage"],[3,5,1,"","BadOptionUsage"],[3,5,1,"","CommandDefinitionError"],[3,5,1,"","CommandParserException"],[3,5,1,"","InvalidChoice"],[3,5,1,"","MissingArgument"],[3,5,1,"","NoSuchOption"],[3,5,1,"","ParamConflict"],[3,5,1,"","ParamUsageError"],[3,5,1,"","ParameterDefinitionError"],[3,5,1,"","ParserExit"],[3,5,1,"","UsageError"]],"command_parser.exceptions.CommandParserException":[[3,3,1,"","code"],[3,2,1,"","exit"],[3,2,1,"","show"]],"command_parser.exceptions.MissingArgument":[[3,3,1,"","message"]],"command_parser.exceptions.ParamConflict":[[3,3,1,"","message"]],"command_parser.exceptions.ParamUsageError":[[3,3,1,"","message"]],"command_parser.formatting":[[4,1,1,"","HelpFormatter"]],"command_parser.formatting.HelpFormatter":[[4,2,1,"","format_help"],[4,2,1,"","format_usage"],[4,2,1,"","maybe_add"]],"command_parser.nargs":[[5,1,1,"","Nargs"]],"command_parser.nargs.Nargs":[[5,2,1,"","satisfied"]],"command_parser.parameters":[[6,1,1,"","Action"],[6,1,1,"","ActionFlag"],[6,1,1,"","BaseOption"],[6,1,1,"","BasePositional"],[6,1,1,"","Counter"],[6,1,1,"","Flag"],[6,1,1,"","Option"],[6,1,1,"","Parameter"],[6,1,1,"","ParameterGroup"],[6,1,1,"","PassThru"],[6,1,1,"","Positional"],[6,1,1,"","SubCommand"],[6,3,1,"","action_flag"]],"command_parser.parameters.Action":[[6,2,1,"","register"],[6,2,1,"","register_action"]],"command_parser.parameters.ActionFlag":[[6,4,1,"","func"],[6,2,1,"","result"]],"command_parser.parameters.BaseOption":[[6,2,1,"","format_usage"],[6,4,1,"","long_opts"],[6,3,1,"","short_combinable"],[6,4,1,"","short_opts"]],"command_parser.parameters.BasePositional":[[6,2,1,"","format_usage"]],"command_parser.parameters.Counter":[[6,3,1,"","accepts_none"],[6,3,1,"","accepts_values"],[6,2,1,"","append"],[6,2,1,"","is_valid_arg"],[6,3,1,"","nargs"],[6,2,1,"","prepare_value"],[6,2,1,"","result"],[6,3,1,"","type"]],"command_parser.parameters.Flag":[[6,3,1,"","accepts_none"],[6,3,1,"","accepts_values"],[6,2,1,"","append_const"],[6,3,1,"","nargs"],[6,2,1,"","result"],[6,2,1,"","store_const"],[6,2,1,"","would_accept"]],"command_parser.parameters.Option":[[6,2,1,"","append"],[6,2,1,"","store"]],"command_parser.parameters.Parameter":[[6,2,1,"","__init_subclass__"],[6,3,1,"","accepts_none"],[6,3,1,"","accepts_values"],[6,2,1,"","format_help"],[6,2,1,"","format_usage"],[6,3,1,"","hide"],[6,2,1,"","is_valid_arg"],[6,3,1,"","nargs"],[6,2,1,"","prepare_value"],[6,2,1,"","result"],[6,4,1,"","show_in_help"],[6,2,1,"","take_action"],[6,3,1,"","type"],[6,4,1,"","usage_metavar"],[6,2,1,"","would_accept"]],"command_parser.parameters.ParameterGroup":[[6,2,1,"","active_group"],[6,2,1,"","add"],[6,2,1,"","check_conflicts"],[6,3,1,"","description"],[6,2,1,"","format_description"],[6,2,1,"","format_help"],[6,2,1,"","format_usage"],[6,2,1,"","maybe_add_all"],[6,3,1,"","members"],[6,3,1,"","mutually_dependent"],[6,3,1,"","mutually_exclusive"],[6,2,1,"","register"],[6,2,1,"","register_all"],[6,4,1,"","show_in_help"]],"command_parser.parameters.PassThru":[[6,3,1,"","nargs"],[6,2,1,"","store_all"],[6,2,1,"","take_action"]],"command_parser.parameters.Positional":[[6,2,1,"","append"],[6,2,1,"","store"]],"command_parser.parameters.SubCommand":[[6,2,1,"","register"],[6,2,1,"","register_command"]],"command_parser.parser":[[7,1,1,"","CommandParser"]],"command_parser.parser.CommandParser":[[7,3,1,"","action"],[7,3,1,"","action_flags"],[7,3,1,"","command"],[7,3,1,"","command_parent"],[7,2,1,"","contains"],[7,3,1,"","formatter"],[7,3,1,"","groups"],[7,2,1,"","has_pass_thru"],[7,3,1,"","long_options"],[7,3,1,"","options"],[7,3,1,"","parent"],[7,2,1,"","parse_args"],[7,3,1,"","pass_thru"],[7,3,1,"","positionals"],[7,3,1,"","short_combinable"],[7,3,1,"","short_options"],[7,3,1,"","sub_command"]],"command_parser.utils":[[8,1,1,"","Args"],[8,1,1,"","ProgramMetadata"],[8,6,1,"","camel_to_snake_case"],[8,6,1,"","format_help_entry"],[8,6,1,"","validate_positional"]],"command_parser.utils.Args":[[8,2,1,"","find_all"],[8,2,1,"","num_provided"],[8,2,1,"","record_action"]],"command_parser.utils.ProgramMetadata":[[8,2,1,"","format_epilog"]],command_parser:[[0,0,0,"-","commands"],[1,0,0,"-","config"],[2,0,0,"-","error_handling"],[3,0,0,"-","exceptions"],[4,0,0,"-","formatting"],[5,0,0,"-","nargs"],[6,0,0,"-","parameters"],[7,0,0,"-","parser"],[8,0,0,"-","utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","property","Python property"],"5":["py","exception","Python exception"],"6":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:property","5":"py:exception","6":"py:function"},terms:{"0":[0,6],"1":[6,8],"2":[3,8],"30":[4,6,8],"abstract":0,"case":6,"class":[0,1,2,4,5,6,7,8],"const":6,"default":[0,6],"do":6,"final":0,"float":6,"function":0,"int":[0,3,4,5,6,8],"return":[0,6],"true":[0,4,6,7,8],A:[0,6],If:[0,6],It:[0,6],The:[0,6],To:0,_:8,__init__:0,__init_subclass__:[0,6],abc:6,abl:0,abov:0,accepts_non:6,accepts_valu:6,action:[0,1,6,7],action_after_action_flag:1,action_flag:[1,6,7],actionflag:[6,7],active_group:6,add:6,add_default:[4,6],alia:6,all:[0,1],allow:[0,1,6],allow_unknown:[0,7],alreadi:0,also:6,altern:0,an:[0,3,6],ani:[0,1,3,4,6,7,8],append:6,append_const:6,ar:[0,1,6],arg:[0,6,7,8],argument:[0,3,6],argv:0,associ:0,author:[0,1,2,3,4,5,6,7,8],auto:0,automat:6,back:6,badargu:3,badargumentusag:3,badoptionusag:3,base:[0,1,2,3,4,5,6,7,8],basecommand:[0,6],baseexcept:2,baseopt:[6,7],baseposit:[6,7],behavior:[0,1],being:0,bool:[0,1,4,5,6,7,8],call:[0,6],callabl:[2,6],camel_to_snake_cas:8,camelcas:6,can:0,check_conflict:6,choic:[0,3,6,8],choicemap:6,chosen:6,classmethod:[0,2,6],clean:6,cli:1,close_stdout:0,cls_handler:2,code:[0,3],collect:[3,6],column:6,combin:[1,6],command:[1,3,4,6,7],command_config:0,command_or_choic:6,command_par:7,command_pars:[0,1,2,3,4,5,6,7,8],commandconfig:[0,1],commanddefinitionerror:3,commandobj:0,commandpars:[0,4,7],commandparserexcept:3,commandtyp:[4,6,7],common:0,compar:0,config:0,configur:[0,1],consid:0,contain:[0,6,7],convert:6,copi:2,core:0,count:5,counter:6,decor:6,defin:0,definit:3,delim:[4,6,8],depend:6,descript:[0,6,8],determin:6,dict:[7,8],directli:[0,6],displai:[0,6],docs_url:8,doe:[0,6],doug:[0,1,2,3,4,5,6,7,8],dure:[0,6],email:8,encount:0,entri:0,epilog:[0,8],error:[0,3],error_handl:0,errorhandl:[0,2],exc:[2,8],exc_typ:2,except:[0,2,8],exclus:6,execut:0,exit:3,explicitli:6,extend:[0,6,8],extended_epilog:4,fals:[0,1,6,7],find_al:8,first:6,flag:6,follow:0,format:[6,7],format_descript:6,format_epilog:8,format_help:[4,6],format_help_entri:8,format_usag:[4,6],formatt:7,forwardref:6,from:[0,6],full:6,func:6,further:6,gener:0,get_handl:2,given:[0,1,6],group:[6,7],group_typ:[4,6],handl:0,handler:[0,2],has_pass_thru:7,have:0,help:[0,6],helpformatt:[4,7],here:[0,6],hide:6,ignor:0,implement:6,includ:6,include_meta:6,index:9,initi:[0,6],instanc:0,instanti:6,instead:0,intend:0,interpret:6,invalid:3,invalidchoic:3,invoc:1,is_valid_arg:6,item:7,iter:6,keyword:[0,6],kwarg:[0,6],level:0,list:[6,7],logic:0,long_opt:[6,7],lpad:8,mai:[0,6],main:0,map:0,maybe_add:4,maybe_add_al:6,member:6,mention:0,messag:[0,3],metavar:6,method:[0,1,6],method_or_choic:6,miss:3,missingargu:3,modul:9,more:0,multipl:1,multiple_action_flag:1,mutual:6,mutually_depend:6,mutually_exclus:6,name:[0,6],narg:6,necessari:[0,6],need:[0,6],none:[0,3,6,7,8],nosuchopt:3,noth:6,num_provid:8,number:0,object:[0,1,2,4,5,6,7,8],omit:[0,6],one:0,onli:[0,6],option:[0,1,2,3,6,7,8],option_str:6,order:6,origin:6,other:[0,6],overrid:0,overridden:6,page:9,param:[3,4,6,8],param_cl:8,param_typ:8,parambas:6,paramconflict:3,paramet:[0,3,7],parameterdefinitionerror:[3,8],parametergroup:[4,6,7],paramorgroup:8,paramusageerror:3,parent:[0,6,7],pars:[0,6],parse_and_run:0,parse_arg:7,parser:[0,3,4],parserexit:3,partial:6,pass:0,pass_thru:7,passthru:[6,7],place:0,point:0,posit:[0,1,6,7],possibl:0,prefix:8,prepar:6,prepare_valu:6,prevent:0,primari:[0,6],prog:[0,8],program:0,programmetadata:8,properti:[0,6],provid:[0,6],rais:0,rang:[5,6],re:0,readi:0,recommend:0,record_act:8,recurs:7,refer:[0,6],regist:[2,6],register_act:6,register_al:6,register_command:6,relat:3,requir:[3,6],resolv:0,result:[0,6],run:[0,1],satisfi:5,search:9,separ:0,sequenc:[0,5,6,8],set:[0,5,6],short_combin:[6,7],short_opt:[6,7],should:[0,6],show:3,show_in_help:6,skip:0,skrypa:[0,1,2,3,4,5,6,7,8],snake_cas:6,so:6,sourc:[0,1,2,3,4,5,6,7,8],specifi:[0,1,6],store:[0,6],store_al:6,store_const:6,str:[0,3,4,5,6,7,8],strai:0,string:6,sub:0,sub_command:7,subclass:[0,6],subcommand:[0,6,7],sy:0,take_act:6,taken:0,text:[0,6,8],thei:[0,1],them:6,thi:[0,6],titl:6,top:0,trigger:0,tupl:[5,6],type:[0,2,6,8],unchang:6,union:[0,1,4,5,6,7,8],unknown:0,unless:0,unregist:2,url:8,us:[0,6],usag:[0,6,8],usage_metavar:6,usageerror:3,util:0,val_count:8,validate_posit:8,valu:[0,3,6,8],version:[6,8],virtual:6,wa:[0,6],wai:6,were:0,what:0,when:[0,6],whether:[0,1,6],which:[0,6],width:[4,6,8],without:6,would_accept:6,wrap:[0,6],you:0},titles:["Commands Module","Config Module","Error_Handling Module","Exceptions Module","Formatting Module","Nargs Module","Parameters Module","Parser Module","Utils Module","Command Parser"],titleterms:{command:[0,9],config:1,error_handl:2,except:3,format:4,indic:9,modul:[0,1,2,3,4,5,6,7,8],narg:5,paramet:6,parser:[7,9],tabl:9,util:8}})