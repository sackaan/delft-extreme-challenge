## Extreminator
For our submission, we have created a way to effectively and consistently label datasets with which a deep learning network can be trained to detect extremist views and foul language. For this, we have used multiple papers to define what extremist views are. We used this to design a platform on which an initial dataset can be labeled. This dataset is then used to train a deep learning network, which will be used to classify future audio segments.

First, we have to get into our definition of extremism.

## Definition of extremism
For our definition of extremism, we have combined different definitions from multiple papers. The papers can be found in our references list. Our definition is as follows:

*** 
*Any spoken content that when taken in its immediate context and excluding neutral quotation or reporting in which the speaker explicitly:*
- *Fosters or justifies prejudice or hostility based on inherent attributes\*;*
- *Promotes an ideology that one group is naturally superior to another one due to inherent attributes\*;
- *Issues direct incitements and threats of violence, or advocates for or glorifies violence;*
- *Affiliates themselves with, recruits for, shows allegiance to or shows admiration towards known extremist entities or groups;*
- *Attempts to spread fabricated misinformation intended to provoke conflict or action in pursuit of a (socio-political) belief or interest/agenda*

*Some related concepts:*
- *Hate speech: An act that attacks or demeans a group/individual based on inherent attributes\*. Relation to extremism: hate speech overlaps with extremist speech but it's not identical.*
- *Supremacism and sectarianism: Ideological categories describing beliefs that think a certain group is (naturally) superior.*
  *Relation to extremism: these are ideological drivers that are subsets of extremism, and thus we flag them.*
- *Terrorism: Systematic use of violence or threats to achieve ideological goals, mainly by trying to induce fear.*
  *Relation to extremism: terrorism closely relates to and generally implies violent action. Extremist speech may promote or praise terrorism.*

*\*Inherent attributes are as follows:*
	- *race*
	- *religion*
	- *nationality*
	- *sexual orientation*
	- *sex*
	- *gender identity*
	- *disability*
	- *social class*
	- *age (unless there is a logical and/or substantiated incentive for prejudice, like no alcohol under 18)*
	- *language*
	- *health status*
	- *political affiliation*
***
## Legal responsibilities
Our definition of extremism closely aligns with the definition of the Dutch General Intelligence Service (AIVD): "*Being ideologically motivated to engage in non-violent and/or violent
activities that undermine the democratic legal order.*" Their definition implies that not all radical or politically charged speech is extremist, so ultra-right or ultra-left parties that still operate within democratic principles are not considered extremist under this definition. We have decided encompass ultra-left and ultra-right speech in our definition of extremism, since we do not want a model to be trained with such language.
From a legal standpoint, our definition aligns with:
- Freedom of expression under Dutch and EU law (Article 7 of the Dutch Constitution and Article 10 of the European Convention of Human Rights);
- Data protection regulations (GDPR): any processing of speech data must comply with privacy laws. This means that we avoid collecting or storing personal data unless necessary and ensure anonymization where it's possible. We are focusing on identifying extremist speech, not profiling speakers or communities. This is very important to avoid violating fundamental rights;
- Restrictions on speech only when it crosses into illegal territory, such as incitement to violence, hate speech, or direct threats.

## Ethical responsibilities
When designing a system that detects extremist or harmful speech, we have to be very careful about how it might affect people. We recognize that language is complex, culturally dependent, and often context-dependent. Our approach tries to stay fair, explainable and human-centered:
- Fairness and bias awareness: AI models can easily pick up hidden biases from the data they're trained on. Our definitions are designed to avoid unfairly targeting any group based on language style, accent or political opinion;
- Respect for people and context: context matters, as quoting a hateful statement in a documentary or academic discussion is not the same as promoting it. Our definition explicitly excludes neutral or educational references by providing context in the initial labeling stage.

## Social responsibilities
The way speech data is collected and used can shape how technology understands and represents people. Because of that, we have a responsibility to make sure our system contributes to a fairer and safer digital environment. We focus on the following areas:
- Building trust: people should be confident that the technology they use isn't biased or politically driven. We aim to make the initial labeling stage clear and fair, so that extremist views or foul language is flagged appropriately.
- Accountability: our labeling system is meant to be open and reviewable. Responsible systems should always allow external oversight and improvement over time.

## Our solution
Our design, which we call Extreminator, makes it easy to consistently label speech as either normal or extremist in an initial dataset. This dataset can be used to train a deep learning network which can automatically detect future extremist speech and foul language.

#### Labelling platform
The first part consists of a web platform in which the people who label data (referred to as "users" in this paragraph) go through a questionnaire in which the questions are designed to detect our definition of extremism. Users can listen to the audio segment of the sentence and read a transcription generated by OpenAI's Whisper. There is a side panel with context for the sentence. This can be generated by any LLM that is trained to create summaries, or we can provide context by showing other sentences in the audio file that have a similar theme. On each question page, the user can immediately flag an audio segment if it is clear that it is extremist speech. The questions are simply included to guide the user in case it isn't immediately clear if an audio segment contains extremist speech. There is also an option to go back to the previous question, in case the user accidentally clicks the wrong button. If an answer to a question implies extremism is found in the audio file, the user receives a pop-up with the question "*Are you sure?*". Clicking "*Yes*" will immediately flag the sentence, and the user will receive the next sentence to be reviewed. If all five questions are answered and no sign of extremism has been found, the sentence is labelled "normal". Sentences are given in random order of audio fragments, to make sure the user doesn't constantly read sentences that are part of the same context.

#### Deep learning based labelling platform
Once an initial dataset has been used to train a deep learning model, the model can be used to classify spoken text. Since we do not have enough knowledge about deep learning models yet, we have decided to create a demo version using Bert, a model developed by Google. An audio file is uploaded and the platform will show each sentence and its classification. Any sentence that is classified as hate or extreme is marked red. Sentences that are marked as normal but have a confidence of ~85% or lower will also be marked red. This threshold may have to be changed, however.

## References
##### Extremism definitions
https://link.springer.com/article/10.1007/s12652-021-03658-z
https://arxiv.org/pdf/2408.16749

##### Legal responsibilities
https://www.aivd.nl/onderwerpen/extremisme
https://gdpr-info.eu/
https://www.denederlandsegrondwet.nl/id/vgrnbj1z0qzw/artikel_7_vrijheid_van_meningsuiting
https://fra.europa.eu/en/law-reference/european-convention-human-rights-article-10