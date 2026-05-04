# Transcript


Transcript. Use arrow keys to navigate between transcript entries. Select an entry to navigate the media to the time of the entry.


Search

AI-generated content may be incorrect

DANES Andrei started transcription

POLMOLEA Andrei
0 minutes 3 seconds0:03
POLMOLEA Andrei 0 minutes 3 seconds
Gonna do something different today. I've never done this before, so it might actually go very bad, but it's recorded so we can laugh afterwards. So today, what is the plan today? We're gonna.

DANES Andrei
0 minutes 13 seconds0:13
DANES Andrei 0 minutes 13 seconds
Yes.

POLMOLEA Andrei
0 minutes 18 seconds0:18
POLMOLEA Andrei 0 minutes 18 seconds
We're gonna build an agent together. I wanted to do this last time. I think it was that week when Claude had a ton of outages, so couldn't really run it last time, but basically it just builds.
POLMOLEA Andrei 0 minutes 35 seconds
On what we spoke about in the first two session when we spoke about the core concepts and then how to build agents. So we're gonna try and build something very simple today. If you have built agents before, I know a bunch of you have.
POLMOLEA Andrei 0 minutes 53 seconds
This is gonna look very, very simple. The idea here with all of these enthusiast sessions is to get everybody at the same kind of or close to the same level. Of course there will be people that are have more expertise in this.
POLMOLEA Andrei 1 minute 7 seconds
And also the way we're going to do it is I'm not just going to show you some code, I'm going to I I wrote some notes and I'm going to essentially write the code with you and try and explain kind of line by line what what it does.
POLMOLEA Andrei 1 minute 25 seconds
But before we go into that, so hackathon, you have all received an e-mail from Marius with a nice GIF in it. And thank you Marius for your design skills with an invitation to register for the May hackathon. So in May.
POLMOLEA Andrei 1 minute 44 seconds
We will run a month long hackathon. Well, month long. I know there's a ton of bank holidays in May, so it's probably 3 weeks hackathon. And the goal in that hackathon is to be part of a team and we'll decide the size of the team.
POLMOLEA Andrei 2 minutes
To target one specific cloud provider. So it might be Azure, it might be WS. We're even considering GCP if if there's interest for that and build an AI agent.
POLMOLEA Andrei 2 minutes 17 seconds
You will have a remit in the hackathon, so we'll start essentially with the requirement and I can already share this with you. It's the requirement will be to build an agent that can do can perform an architecture review on an application.
POLMOLEA Andrei 2 minutes 34 seconds
You will have some starting documentation for the application. I'm not gonna spoil the surprise for later, but basically you have a starting point and you need to build an agent. You can go as deep or as crazy as you want with that agent.
POLMOLEA Andrei 2 minutes 50 seconds
Throughout the month we will have sessions with the CSPS where they will talk about the technology. We will also have office hours where you will be able to show your progress and also ask questions. And at the end we will be able to present the agents and essentially compare see see essentially what the difference.
POLMOLEA Andrei 3 minutes 10 seconds
Are and in what directions people have gone into. You need to register for this, so please register. The form does ask you for a preference for CSP. I cannot guarantee you'll be in a team that is your first preference of CSP. I see there up to now have been quite a lot of.
POLMOLEA Andrei 3 minutes 28 seconds
There has been quite a lot of interest in Azure, so we need to split a little bit. But yeah, I think that's that's the idea. You will be expected to write code during this, right? So if that's not something that you necessarily do as part of your job or are interested in.
POLMOLEA Andrei 3 minutes 48 seconds
Then maybe this is not necessarily for you, but yeah, it is a technical, essentially a technical assignment and at the end of the month kind of our goal with this is that you are able to build an agent. That's it. Any any questions on this? Anything I can clarify?
POLMOLEA Andrei 4 minutes 10 seconds
No, OK.

DENIES Arnaud
4 minutes 13 seconds4:13
DENIES Arnaud 4 minutes 13 seconds
Andrea, I'm not speaking. So maybe if you can illustrate the logistic behind it in term of, you know, you said three weeks or one month longer. So maybe if you could give examples how frequently should people meet or?
DENIES Arnaud 4 minutes 31 seconds
How it will be organized very, very concretely. Maybe it will help people decide if they should be part of it or not.

POLMOLEA Andrei
4 minutes 37 seconds4:37
POLMOLEA Andrei 4 minutes 37 seconds
Yeah, yeah, sure. That's a good point, Arun. Thank you. So, so it's a remote hackathon. We you want to be co-located. We will consider if we can actually have something at the end of the month to have people co-located in enjoy and potentially in in in Asia.
POLMOLEA Andrei 4 minutes 55 seconds
Uh.
POLMOLEA Andrei 4 minutes 57 seconds
Every week of the month we will have office hours, so that's a session that you need to essentially attend to show your progress and ask questions. That's essentially an hour long session.
POLMOLEA Andrei 5 minutes 13 seconds
We will also have a few ad hoc sessions with the CSPs that depending on whether you're working on Azure or AWS, you will have some sessions specifically on those to describe the technology. Again, those are probably gonna be one or two hours.
POLMOLEA Andrei 5 minutes 30 seconds
Essentially throughout the month and everything else is ad hoc. So you're in a team and you can essentially decide to meet as frequently or as infrequently as you want to split the work and you have to go through the entire lifecycle of an agent. So you have to take the requirements.
POLMOLEA Andrei 5 minutes 49 seconds
Do the planning first, obviously, then plan your tasks and divide them amongst yourselves and you decide how deep you want to go with this. There will be some hints, of course, so there's gonna be some guidelines and.
POLMOLEA Andrei 6 minutes 5 seconds
In what directions you can go because it's a hackathon and it's essentially scripted a little bit, but you will have opportunities to do things outside of what is required you will get.
POLMOLEA Andrei 6 minutes 21 seconds
An account or a subscription, a sandbox account or subscription where you can work in directly all of you. And yeah, I think that's that's pretty much it. I don't know if I'm missing something. The time expectation I think is around.
POLMOLEA Andrei 6 minutes 39 seconds
10% of your your time throughout the month, the working month. So that's kind of minimal. Of course, if you want to, if you're really passionate and you want to work more, that's that's great, but minimal to have something viable in a team.
POLMOLEA Andrei 6 minutes 56 seconds
I think it's expected that you spend about 10% of your time on this, including the sessions and everything that we have planned.

MUELLER Marius
7 minutes 5 seconds7:05
MUELLER Marius 7 minutes 5 seconds
Maybe Andre, just to confirm when you'll be able to share like the timing, I think there are a couple of dedicated days where you plan to be yourself in Enjoy and probably where some of the hackathon attendees also should be in Enjoy. Are you already able to share like this kind of timing timeline that?
MUELLER Marius 7 minutes 25 seconds
Plan.

POLMOLEA Andrei
7 minutes 26 seconds7:26
POLMOLEA Andrei 7 minutes 26 seconds
So, so I think we'll try and be co-located towards the end of the month. So in the last week of May we'll be co-located. I'm trying to time that right before the the presentation at the end and the other presentations from the CS PS and everything.
POLMOLEA Andrei 7 minutes 42 seconds
That's why it's really important to fill in the form. I really need the final numbers so they can actually arrange all the sessions and everything. So the the Azure and AWS have both confirmed they can do the sessions, but they need some some numbers and some guidelines on who's gonna attend.
POLMOLEA Andrei 8 minutes 1 second
So we'll we'll schedule that in the next, uh, next few days.

MUELLER Marius
8 minutes 5 seconds8:05
MUELLER Marius 8 minutes 5 seconds
Sounds good. Thank you.

POLMOLEA Andrei
8 minutes 10 seconds8:10
POLMOLEA Andrei 8 minutes 10 seconds
OK, so let's let's move on. Let's let's build a simple agent. What are we going to do? We're just going to take an agent that is, let's say, an A WS expert, because I just happen to be an A WS guy, but it doesn't have to be that.
POLMOLEA Andrei 8 minutes 28 seconds
There's only one small part which is AWS specific, and I'll explain why it's AWS specific and how you can make it not AWS specific. We're going to use Langchain. Why are we going to use Langchain? Essentially attacks that we're gravitating towards Langchain is our default agentic framework. There's plenty of.
POLMOLEA Andrei 8 minutes 47 seconds
These framework frameworks. So we're gonna use Linechain because that's essentially even for the hackathon what you will you will need to use.
POLMOLEA Andrei 8 minutes 56 seconds
We'll add memory with. This is the AWS specific bit, so we'll use Bedrock there because it's a lot quicker to to set up. We'll add a tool to the agent so it's the bit that performs the actual work and we'll just have throughout the the session. We'll just send some messages to the LLM. It's not a crazy conversation.
POLMOLEA Andrei 9 minutes 16 seconds
It's all going to be done programmatically, you know, from my machine, but it's what you would probably do for any really any use case that you have. This is how you get started with any agentic use case. Of course, these agents can go a million times more complicated than this.
POLMOLEA Andrei 9 minutes 34 seconds
But you usually start with with a framework which is similar to what I'm about to show you. So get started on on your machine. You typically need a few things on your machine. You typically need VS code for anything to do with it, and I'm sure most of you have this.
POLMOLEA Andrei 9 minutes 51 seconds
You need the terminal. You can use it in VS code. I I'm using it separately because I can make this the text a little bit bigger and you need Python and a tool called UV which allows you to to manage Python packages.
POLMOLEA Andrei 10 minutes 6 seconds
So that's really it. On the AWS side, I do have an AWS account with credentials set up. I'm gonna walk you through the model selection and the memory side of things as well. So the first thing that we need to do, I have a folder which is I have.
POLMOLEA Andrei 10 minutes 26 seconds
Some notes there, but it's pretty much empty. When you start, you initialize your project. So UV is a great tool. By the way, if you haven't done a lot of Python work, UV is a great tool to manage. It's very fast and we will add some packages. I'm going to Add all of them. In the beginning I'm going to explain.
POLMOLEA Andrei 10 minutes 46 seconds
A few things about the different packages that we add. So Auto 3 is the AWS package, not really relevant for here. We're gonna use it as part of the tool. Landchain is our agentic framework.
POLMOLEA Andrei 11 minutes 2 seconds
Lang Chain AWS is a set of extensions for using AWS services with Lang Chain and Lang graph.
POLMOLEA Andrei 11 minutes 14 seconds
Check. Let me also try and spell correctly. Land graph check checkpoint AWS is a set of primitives as part of land graph. So the interesting bit here.
POLMOLEA Andrei 11 minutes 30 seconds
Langchain is we call it Langchain. It it's becoming this this behemoth with a lot of different components to it and I'm already mentioning here Langraph and Langchain. So I opened an image from Reddit to show you the differences here.
POLMOLEA Andrei 11 minutes 46 seconds
This is what they kind of offer. Lanchain is the the easiest way to get started. It's a React agent framework where you can build an agent where you send a message, it reasons, and it acts on your behalf. It's really kind of standardized. It doesn't let you customize too many things.
POLMOLEA Andrei 12 minutes 5 seconds
And it's similar to other libraries that you might have used. Crew, you know, Open AI, the SDK from Open AI, Strands from AWS, a lot of them. Langraph is a set of primitives, so Langen is built on top of Langraph.
POLMOLEA Andrei 12 minutes 24 seconds
And it's a set of primitives where you build much more complex agents, typically agents where you have a workflow. So if you're used to kind of tools in which you build workflows, right? So you chain a series of steps.
POLMOLEA Andrei 12 minutes 40 seconds
This is kind of kind of like that. So it really this is useful where you want to have an agent that does not just interact with LLM but also.
POLMOLEA Andrei 12 minutes 55 seconds
Does other steps, so maybe it performs some scripted tasks and some of the tasks might actually be using an LLF. So it's it's a lower level implementation and deep agents are kind of more complex or not necessarily complex, but they're built with.
POLMOLEA Andrei 13 minutes 15 seconds
Skills and file system usage in mind and sub agent architectures. So they're they're this is a framework for kind of building an agent that takes.
POLMOLEA Andrei 13 minutes 31 seconds
That uses more advanced functionalities of the LLMS like planning for example, as I said, file system usage, skills and so on. So a bit confusing, but we're primarily using Limechain right now, so I've installed my.
POLMOLEA Andrei 13 minutes 48 seconds
My packages. Now if we look here, when I initialize this, I already have some code here. Let's just get this deleted and really now I have some notes here just to get us started a little bit, so just so I don't have to actually.
POLMOLEA Andrei 14 minutes 8 seconds
Type everything. I'm importing createagent function which is something that Langchain gives you. This is the easiest way to create an agent, a React agent, and you just have to give it some configuration.
POLMOLEA Andrei 14 minutes 23 seconds
The Bedrock Converse integration allows me to use Claude in this case from a WS and a side note here we will try and create an integration with secure GPT here so that you can just import the secure GPT model.
POLMOLEA Andrei 14 minutes 42 seconds
Then I defined 2 variables, my AWS region and I don't have to explain this and the LLM model. So this you have a series of models you can use. You can also use for example in Azure you can use an open AI model.
POLMOLEA Andrei 14 minutes 59 seconds
You can use Mistral models. All of them have identifiers and in this case I'm I'm using Sonnet 44.5 in the EU region in in a WS now.
POLMOLEA Andrei 15 minutes 16 seconds
Let's let's define a system prompt. So what system prompts are essentially the text that you give the agent at the start of a conversation. It's really like a message that gets passed to to an agent. Now it's important to note that this consumes your tokens, right? So it consumes your your context.
POLMOLEA Andrei 15 minutes 35 seconds
You shouldn't make these too complex. That's why we have or not we, but the community has created skills which allow you to expand the system prompts dynamically and not put.
POLMOLEA Andrei 15 minutes 51 seconds
All your instructions in a single string. And by the way, if you have any questions, please stop me at at any time. I'm trying to explain every every line, but if you have any questions about any of these topics, let me know.
POLMOLEA Andrei 16 minutes 7 seconds
Typically when you write a system prompt, you mention the role first. You say what are you? You are an AWS engineer, an Azure engineer. You are a cloud broker. You are an insurance broker. You can also tell it.
POLMOLEA Andrei 16 minutes 23 seconds
How to answer in what tone? So in this I'm just saying factually, but you can you can say be more candid, be very direct, things like that that inform the agent on how to actually respond to the end user.
POLMOLEA Andrei 16 minutes 43 seconds
And let's write a user prompt as well. So what will the user ask? So what is cloud formation? I'm just getting this ready. Normally if you were to build an agent with the chat bot interface for example, this would come from that chat bot.
POLMOLEA Andrei 17 minutes 3 seconds
But in this case, I'm just writing a static string here just to show you some kind of message. Now let's configure our LLM. So chat bedrock converse.
POLMOLEA Andrei 17 minutes 17 seconds
And then we're going to use the model ID that I just gave you. So every model has an ID. We're just passing this on to Chadbedrawconverse. We're going to set the the region name to the AWS region.
POLMOLEA Andrei 17 minutes 37 seconds
And now temperature. So this is a measure of how creative an agent can be. If if you are, if you set it to 0, the agent is is just gonna.
POLMOLEA Andrei 17 minutes 51 seconds
Give you kind of the best answer it can give you. It's not going to go too crazy on the answers. It's not going to. You know, when we spoke in the first first presentation, we looked at how it chooses the next token to predict. When it's zero, it usually chooses the first kind of option when you're close.
POLMOLEA Andrei 18 minutes 11 seconds
To one, it's a little bit more creative, so your answers vary a little bit. It's it's nicer for, for example, for creative writing you would set the temperature higher. For very factual writing, you would set the temperature lower. I set it to .3 here. You can you can play around with this. It doesn't have as much of an influence as.
POLMOLEA Andrei 18 minutes 31 seconds
As you would think essentially. So it's a small variation, but it's still noticeable. Now let's create our agent. So when you create your agent, this framework allows you to again, as I said, very very easy way to create a React agent if you were to do it in Landgraf.
POLMOLEA Andrei 18 minutes 50 seconds
This would take you many, many more steps. You would have to model it node by node. This just gives you a function and you just have to configure the LLM here. We're gonna give it the system prompt as well, so we're just gonna.
POLMOLEA Andrei 19 minutes 9 seconds
Set what we the string that we created here. And I'm sorry this this window is quite big, but I also wanted you to see the text, so it's a trade-off. OK, so that's all we will do for now. We'll see that maybe later we will do something else.
POLMOLEA Andrei 19 minutes 26 seconds
So this expects this agent expects messages in a specific format, which I just happened to have noted on a piece of paper. So you don't. Obviously nobody would learn this, but you can.
POLMOLEA Andrei 19 minutes 44 seconds
Give the agent here a list of messages. You can have historical messages as well as part of this list. That's why you're not just giving it a prompt, you're giving it a little bit more information. You also see who actually wrote that message because you can have messages.
POLMOLEA Andrei 20 minutes 3 seconds
That are written by another agent essentially, or the agent in this case so.
POLMOLEA Andrei 20 minutes 12 seconds
We are just using the the prompt that we set up here and we're just we're just gonna create the response. So let's just create it like this because I might actually.
POLMOLEA Andrei 20 minutes 28 seconds
End up having to do something. So agent dot invoke. This is how you invoke your agent. That's it. That's all you need to do. You need to give it the messages. That's it. And let's now print the response like this so it's a little bit easier.
POLMOLEA Andrei 20 minutes 43 seconds
This gives you the response that comes back from the agent is again a historical representation of all your messages. So we're gonna take the last message and just just print its content.
POLMOLEA Andrei 21 minutes
So I think this is, uh, it. I'm just looking through my my notes.
POLMOLEA Andrei 21 minutes 8 seconds
OK, let's just try and it'll it'll tell us um UV run main dot by.
POLMOLEA Andrei 21 minutes 16 seconds
So let's see what happens here. Again, as I said, apart from the the user prompt here, which is hard-coded, you could have this user prompt, you know, coming from the terminal or coming from an interface or from wherever else. But this is an agent here, right? So it's it's a minimal agent, but it's an agent nonetheless.
POLMOLEA Andrei 21 minutes 35 seconds
Let's see if it if it actually runs and if I run into the same Claude when when we tried to do this last time, all the Claude models were having a very weird week.
POLMOLEA Andrei 21 minutes 51 seconds
OK, so it gave me an answer. You know it describes what transformation is, which is essentially what what I asked it. Now I want to to do something else. I want to ask how does it compare to?
POLMOLEA Andrei 22 minutes 11 seconds
Other tools and I'm gonna run the agent again and see. Let's see how Cloudformation compares to to other tools. Again, here it's really nice because it it gave me kind of a formatted response. It's not just giving you a.
POLMOLEA Andrei 22 minutes 26 seconds
Two sentence response. So it's really nice. It went into common use cases. OK, so now let's see. I'd be happy to help you with compare tools, but I need more context about what specific tool or service you're asking about. So what is happening here?
POLMOLEA Andrei 22 minutes 40 seconds
The agent is does not remember what I asked it previously, does not remember that I asked about cloud formation. It just remembers it. It just sees the the prompt.
POLMOLEA Andrei 22 minutes 55 seconds
That I gave it right? So every invocation of the agent without memory is essentially just sending this this string plus this string to the LLM and letting it decide what to what to do as a React agent.
POLMOLEA Andrei 23 minutes 12 seconds
So that's why we need memory to allow users to chain chain messages like this. So let's change it back because we will do something different here.
POLMOLEA Andrei 23 minutes 25 seconds
So I'm gonna copy some more stuff from here.
POLMOLEA Andrei 23 minutes 30 seconds
And I'll I'll explain a little bit about what we're doing here. So I'm I'm gonna set up memory for this agent. I'm gonna use the Bedrock an integration with Bedrock. Now I'll show you here what I have created. So in in the agent core interface.
POLMOLEA Andrei 23 minutes 49 seconds
Anyway, hit logged me out, but I created a new memory. It's a short term memory. I just click create and use the default parameters. I didn't change anything. Now you don't have to use this. You don't have to use an AWS memory provider here.
POLMOLEA Andrei 24 minutes 7 seconds
You have in land chain you have a series of of providers built in and of course you can build your own. You can save it in memory, you can do SQL lite integrations and for production you would typically use something like Postgre, SQL, Mongo DB, something like this.
POLMOLEA Andrei 24 minutes 27 seconds
So that's that's the beauty of it. You can you essentially can swap these. Ultimately in Lang chain a checkpoint is a checkpoint. It's a a mark at the specific point in the graph, in this case in our when we send a message.
POLMOLEA Andrei 24 minutes 44 seconds
Where we save that state, right? So when we receive a message from the user, we save it. When we receive a response from the agent, we save it. So we essentially build up that that knowledge and you're bound by the context limit of the agent.
POLMOLEA Andrei 25 minutes 1 second
But you're also bound by, you know, whatever settings you have in your memory. So if you're here, you have 90 days expiration, so it's not gonna remember things beyond beyond 90 days, so.
POLMOLEA Andrei 25 minutes 17 seconds
We've added the memory ID. That's that's all essentially all you need to do. Now we also need to create a session. I'm just gonna create a mock up session ID here because life's too short. I think you need at least 36.
POLMOLEA Andrei 25 minutes 36 seconds
Or 32 characters for Bedrock. I think there is a.
