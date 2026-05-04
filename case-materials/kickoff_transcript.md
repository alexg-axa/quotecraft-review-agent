# Transcript

Okay, good morning, everyone, and thanks for joining in such high numbers and earlier than the call was scheduled for. So really appreciate it. We have to start with a kind of a Starward reference. So may the force be with you on this hackathon. I really hope we're all going to have fun.
POLMOLEA Andrei 0 minutes 38 seconds
It's the first time we're organizing this inside the cloud broker team and I think internally in the cloud view. So really hope it's going to go okay. One really important thing like we did this morning, if you find any issues with anything that I'm saying or with any of the materials, please flag them as soon as we can.
POLMOLEA Andrei 0 minutes 57 seconds
It's a month, so we have a lot of time to fix things and, um, and you know, make them better.
POLMOLEA Andrei 1 minute 5 seconds
The goal of this hackathon is quite simple, I think. Initially, when we planned it just for the cloud broker team, obviously it got extended to a wider audience. But the idea was pretty simple. It was for our community, AI enthusiast community, to gain some hands-on experience with building AI agents.
POLMOLEA Andrei 1 minute 24 seconds
Not, you know, the typical traditional experience that you get in those immersive days, for example, from the CSPs, where you click some buttons, it's all scripted, it's all, you know, pre-prepared, and it goes well, but at the end of the day, you don't really know what you've done.
POLMOLEA Andrei 1 minute 44 seconds
The idea was to try and have as close to a real environment to build an agent as possible, hit some roadblocks, be creative with it. So therefore, it's not going to be extremely scripted. It's going to be quite wide open. And hopefully all of us together will
POLMOLEA Andrei 2 minutes 6 seconds
gather enough best practices out of this. So as a business unit, we can go ahead and build agents. The additional thing that I kind of I want out of this, of course, I don't think everybody will build agents every day at their job. I think I would like us to be confident enough and myself included.
POLMOLEA Andrei 14 minutes 53 seconds
new terms that I'm using now. Do you want to use rag? Do you not want to use rag? I'll give you here kind of the way I would approach this.
POLMOLEA Andrei 15 minutes 6 seconds
I wouldn't, I would probably spend now a few to three days, obviously you have the presentation from the CSP, just going through the materials, trying to plan a little bit, communicate with your team, trying to plan what you will do. And for the first, you know, until next week, I would try and get something very basic, very simple running, even if it's on your local laptop.
POLMOLEA Andrei 15 minutes 28 seconds
You know what I showed in the demo of the last enthusiast session, which hopefully you've all watched. Just get, you know, an agent there with a system prompt, maybe a tool, something very basic running that can produce an output, which is not necessarily a presentation or a PDF yet. It can be some text.
POLMOLEA Andrei 15 minutes 48 seconds
That bit, you're already done if you're doing that, right? So your agent already meets the requirements. And then you can add to it. Maybe then you can add, you know, RAG, maybe then you can add a code scanning tool. Maybe you can have a PDF or a PPT generator at the end to create a nice report.
POLMOLEA Andrei 16 minutes 7 seconds
For it, but I would, I would try and move really quickly with something extremely basic, and there are planted issues in the materials that I gave you.
POLMOLEA Andrei 16 minutes 18 seconds
Note, I can already guarantee you this, no team will get all of them. It's very difficult. Some are extremely difficult to find. The idea is to find something that you can say, this is what you should improve. And that's already meeting the spec because this is not, doesn't need to be a comprehensive agent. But get something.
POLMOLEA Andrei 16 minutes 37 seconds
running really fast. And what this will allow us, we can then go to the CSPs. And if you have, if you want to dive deeper into an area like RAG, like, you know, tool usage or a multi-agent system, then we can ask them to do like a dedicated session on that so they can, you know, upscale you directly in the area that you need.
POLMOLEA Andrei 16 minutes 57 seconds
This is what I would do. Of course, if you want to spend a little bit more time planning and then do a big push to write the code, you can also do that.
POLMOLEA Andrei 17 minutes 5 seconds
Uhh.
POLMOLEA Andrei 17 minutes 6 seconds
About the findings.
POLMOLEA Andrei 17 minutes 8 seconds
Please try and have, you know, take it a little bit seriously and have like some, you know, complex findings, right? So I gave you here some examples. Deployment has replicas one, which is bad. You should have more replicas. I don't need to see the app. I can just, you know, write some dummy.
POLMOLEA Andrei 17 minutes 29 seconds
OpenShift recommendations and I get that. That's not the goal of this. The goal of this is to actually look at the materials and try and put them together, right? And only by putting them together, you will be able to reference a policy, reference
POLMOLEA Andrei 17 minutes 47 seconds
specifics of your application. Otherwise, if you just, you can just type in an LLM, give me OpenShift recommendations, and you'll get all of those.
POLMOLEA Andrei 17 minutes 58 seconds
So that's it. I think I tackled everything.
POLMOLEA Andrei 18 minutes 5 seconds
I will of course share, you have the recording and share the presentation, but a lot of this now rests on reading the materials.
POLMOLEA Andrei 18 minutes 14 seconds
Now, at the very high level, do you have any questions, any immediate thoughts that you have that I can respond to right now?
POLMOLEA Andrei 18 minutes 30 seconds
OK.

VEEVAETE Tommy
18 minutes 31 seconds18:31
VEEVAETE Tommy 18 minutes 31 seconds
Maybe just a small thing with how are we getting access to the accounts on Azure and AWS.

POLMOLEA Andrei
18 minutes 37 seconds18:37
POLMOLEA Andrei 18 minutes 37 seconds
Okay, actually, you see I had this on my list. So I think I'll ask, I don't know if Ali is on the call, if he has given you access to the resource group on Azure. Everybody on in the AWS teams should have a hackathon account, sandbox account already with their privileged AXA IDP.
POLMOLEA Andrei 18 minutes 57 seconds
So you should be able to log into AWS right now. The account is called something.

VEEVAETE Tommy
19 minutes 3 seconds19:03
VEEVAETE Tommy 19 minutes 3 seconds
Let me check for you.

POLMOLEA Andrei
19 minutes 7 seconds19:07
POLMOLEA Andrei 19 minutes 7 seconds
For Azure, you mean?

VEEVAETE Tommy
19 minutes 10 seconds19:10
VEEVAETE Tommy 19 minutes 10 seconds
AWS, I'm on the AWS team. We'll begin now and I can let you know in one second.

POLMOLEA Andrei
19 minutes 13 seconds19:13
POLMOLEA Andrei 19 minutes 13 seconds
Okay.
POLMOLEA Andrei 19 minutes 16 seconds
Yeah, you should have, and the account name is has hackathon in it, but I generated some team. Okay. Okay, so, well, I'll confirm with Ali on the resource groups as well. I think you should have access to those as well.

VEEVAETE Tommy
19 minutes 22 seconds19:22
VEEVAETE Tommy 19 minutes 22 seconds
Yeah, perfect. I see it.
LA
LOTFI Ali
19 minutes 34 seconds19:34
LOTFI Ali 19 minutes 34 seconds
Yeah, it's the I confirm on the way.

POLMOLEA Andrei
19 minutes 35 seconds19:35
POLMOLEA Andrei 19 minutes 35 seconds
Again.
POLMOLEA Andrei 19 minutes 37 seconds
Okay.
POLMOLEA Andrei 19 minutes 38 seconds
Thanks, Ali.
LA
LOTFI Ali
19 minutes 38 seconds19:38
LOTFI Ali 19 minutes 38 seconds
If someone has any trouble to access, please feel free to reach me.

POLMOLEA Andrei
19 minutes 45 seconds19:45
POLMOLEA Andrei 19 minutes 45 seconds
But as I said, spend some time with the materials and talking to the team.
POLMOLEA Andrei 19 minutes 51 seconds
I think you won't have something to deploy on the CSPs for a while, for a few days.

VEEVAETE Tommy
19 minutes 56 seconds19:56
VEEVAETE Tommy 19 minutes 56 seconds
Not true.

POLMOLEA Andrei
20 minutes 1 second20:01
POLMOLEA Andrei 20 minutes 1 second
Okay.

KRAUSE Karin
20 minutes 2 seconds20:02
KRAUSE Karin 20 minutes 2 seconds
Andrei, one question. I think at least I tried to register myself on the hackathon, but it looks like I have been not respected. I'm not part of a team. I'm only here because I asked Argo to invite me. I have never heard anything back, so maybe I was too late, I don't know, but

POLMOLEA Andrei
20 minutes 19 seconds20:19
POLMOLEA Andrei 20 minutes 19 seconds
Okay.

KRAUSE Karin
20 minutes 23 seconds20:23
KRAUSE Karin 20 minutes 23 seconds
It would be nice if I could also take part.

POLMOLEA Andrei
20 minutes 26 seconds20:26
POLMOLEA Andrei 20 minutes 26 seconds
Okay.
POLMOLEA Andrei 20 minutes 29 seconds
Andrei and Marius said, I don't know, can you check it?
POLMOLEA Andrei 20 minutes 34 seconds
The registration for Koren.

DANES Andrei
20 minutes 36 seconds20:36
DANES Andrei 20 minutes 36 seconds
Yeah, Marius, Marius is off. I had a look, so we closed the registration already, but I replied. So if it's okay, you, because I know you created already the accounts, if it's if it's fine from your side, for sure, no, no issue. Sorry, because I wasn't involved in the, yeah, yeah.

POLMOLEA Andrei
20 minutes 49 seconds20:49
POLMOLEA Andrei 20 minutes 49 seconds
Yeah, just tell me which group. Just tell me which group, because I need to add Karen's access. But other than that, I mean, again, the AWS access is not that critical. The most important thing is having access to the materials, which you should have.

KRAUSE Karin
21 minutes 7 seconds21:07
KRAUSE Karin 21 minutes 7 seconds
Okay, cool. Thanks.

DANES Andrei
21 minutes 8 seconds21:08
DANES Andrei 21 minutes 8 seconds
Yeah.

POLMOLEA Andrei
21 minutes 9 seconds21:09
POLMOLEA Andrei 21 minutes 9 seconds
And when you divide the work, so another point to note. I agreed with Olivier and Thomas and Malik to try and limit the amount of time that is being spent on this. I think we said about two days for every person. That's why there are so many people in the team, including the calls that you're going to have. This means
POLMOLEA Andrei 21 minutes 29 seconds
that you should try and divide the work. So if you need to have to build some tools, for example, divide the work, have one person build a tool, have another person build another tool, somebody writing the system prompt. Really, it's not going to take that much work here. So there's going to be a little bit of overhead to communicate with the members of your team.
POLMOLEA Andrei 21 minutes 51 seconds
But try and divide the work and make sure that you also communicate with each other so that everyone understands the whole code base. I have created GitHub repositories for each team, so you should have access to GitHub repository.
POLMOLEA Andrei 22 minutes 10 seconds
on github.axa.com. Bear in mind that your sandbox accounts are not connected to the AXA environment, so you will not be able to do any CICD type stuff. If you really want to do CICD and automated deployments, even though my recommendation is to try and focus on the agent, not fancy deployments.
POLMOLEA Andrei 22 minutes 30 seconds
But if you want to do that, you can create a repository on GitHub.com and use that. But again, my recommendation is to try and focus on the agent and deploy it manually. We're not trying to show that we can do, you know, fancy deployments here.
POLMOLEA Andrei 22 minutes 50 seconds
Anything else?
POLMOLEA Andrei 22 minutes 54 seconds
Okay, so I'll let you, I'll reach out throughout. If you guys don't write on the team's channel, I'll reach out to you. We have the sessions tomorrow and Wednesday, and I really hope, you know, towards the end of the week that all of you guys.
POLMOLEA Andrei 23 minutes 13 seconds
have a plan and from next week we can actually help you help you get get building.