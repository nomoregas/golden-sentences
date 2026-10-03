"""Source for data/sentences.json. Run tools/make_data.py to regenerate.

Every sentence is written for der Apfel, with the parts that depend on the
object's gender in braces. make_data.py fills them in for each object in
NOUNS (masculine, feminine, neuter), so one template gives three versions.
Placeholders work in the German, the English, the token glosses, the note,
the hint and the common mistake; see FORMS for the full list.

Each token is  word:gloss:case:field
  gloss  literal English, underscores for spaces
  case   N (nominative) A (accusative) D (dative) G (genitive) v (verb) - (none)
  field  position in the German sentence frame:
         KF  und/aber slot before the sentence
         VF  Vorfeld (the one element before the verb)
         LK  left bracket (conjugated verb, or dass/weil in a verb-final clause)
         MF  Mittelfeld
         RK  right bracket (infinitive, participle, separable prefix)
         NF  Nachfeld (clauses trailing after the bracket)
"""

# The swappable object, one per gender. Everything in the story is about it.
NOUNS = {
    "m": {"label": "der Apfel", "en": "apple"},
    "f": {"label": "die Birne", "en": "pear"},
    "n": {"label": "das Bonbon", "en": "sweet"},
}

# Placeholder → (masculine, feminine, neuter)
FORMS = {
    # the noun
    "Apfel": ("Apfel", "Birne", "Bonbon"), "Äpfel": ("Äpfel", "Birnen", "Bonbons"),
    # articles and determiners
    "Der": ("Der", "Die", "Das"), "der": ("der", "die", "das"), "den": ("den", "die", "das"),
    "ein": ("ein", "eine", "ein"), "einen": ("einen", "eine", "ein"), "keinen": ("keinen", "keine", "kein"),
    "seinen": ("seinen", "seine", "sein"), "roten": ("roten", "rote", "rote"),
    # pronouns standing for the object
    "Er": ("Er", "Sie", "Es"), "er": ("er", "sie", "es"), "ihn": ("ihn", "sie", "es"),
    "meiner": ("meiner", "meine", "meins"), "keiner": ("keiner", "keine", "keins"), "einer": ("einer", "eine", "eins"),
    "Welchen": ("Welchen", "Welche", "Welches"), "welchen": ("welchen", "welche", "welches"),
    # words for the notes
    "masculine": ("masculine", "feminine", "neuter"),
    "der→den": ("der becomes den", "die stays die", "das stays das"),
    "weak": ("-en", "-e", "-e"),
    "sein-ending": ("takes -en: seinen, like einen", "takes -e: seine, like eine", "takes no ending: sein, like ein"),
    "plural-rule": ("the plural adds an umlaut", "the plural adds -n", "the plural adds -s"),
    # English
    "apple": ("apple", "pear", "sweet"), "apples": ("apples", "pears", "sweets"), "an": ("an", "a", "a"),
}

SETS = {
    "ferriss": "Ferriss core",
    "golden": "Golden expansion",
    "extra": "Gap fillers",
}

S = []


def s(key, set_, source, en, de, toks, topics, note, hint, mistake=None):
    S.append(dict(key=key, set=set_, source=source, en=en, de=de, toks=toks,
                  topics=topics, note=note, hint=hint, mistake=mistake))


# --------------------------------------------------------------------------
# Tim Ferriss's original deconstruction sentences (13, as in his video)
# --------------------------------------------------------------------------
s("F1", "ferriss", "Ferriss #1", "The {apple} is red.", "{Der} {Apfel} ist rot.",
  "{Der}:the:N:VF {Apfel}:{apple}:N:VF ist:is:v:LK rot:red:-:MF",
  ["gender-articles", "predicate-adjective"],
  "{Apfel} is {masculine}, so 'the' is {der}. After ist, the adjective takes no ending.",
  "{Apfel} is {masculine}.")
s("F2", "ferriss", "Ferriss #2", "It is John's {apple}.", "Es ist Johns {Apfel}.",
  "Es:it:N:VF ist:is:v:LK Johns:John's:G:MF {Apfel}:{apple}:N:MF",
  ["genitive-s"],
  "Names take -s for possession, with no apostrophe: Johns {Apfel}.",
  "No apostrophe in the possessive.",
  {"wrong": "Es ist John's {Apfel}.", "why": "German doesn't use an apostrophe here: Johns."})
s("F3", "ferriss", "Ferriss #3", "I give John the {apple}.", "Ich gebe John {den} {Apfel}.",
  "Ich:I:N:VF gebe:give:v:LK John:John:D:MF {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["dative-accusative", "verb-second"],
  "The {apple} is the thing given, so it's accusative: {der→den}. John receives it (dative). With two nouns, the dative comes first.",
  "The {apple} is the object: accusative.")
s("F4", "ferriss", "Ferriss #4", "We give him the {apple}.", "Wir geben ihm {den} {Apfel}.",
  "Wir:we:N:VF geben:give:v:LK ihm:him:D:MF {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["personal-pronouns", "dative-accusative"],
  "ihm is 'him' in the dative, the one receiving. {den} {Apfel} is the accusative object.",
  "'him' as the receiver is dative.")
s("F5", "ferriss", "Ferriss #5", "He gives it to John.", "Er gibt {ihn} John.",
  "Er:he:N:VF gibt:gives:v:LK {ihn}:it:A:MF John:John:D:MF",
  ["stem-vowel-change", "pronoun-gender", "pronoun-order"],
  "geben becomes gibt for er/sie/es. 'It' is the {apple} ({masculine}), so it's {ihn}. A pronoun object comes before a noun object.",
  "'it' = {der} {Apfel}, and geben changes its vowel.",
  {"wrong": "Er gibt John {ihn}.", "why": "A pronoun object goes before a noun object: {ihn} John."})
s("F6", "ferriss", "Ferriss #6", "She gives it to him.", "Sie gibt {ihn} ihm.",
  "Sie:she:N:VF gibt:gives:v:LK {ihn}:it:A:MF ihm:him:D:MF",
  ["pronoun-order", "personal-pronouns"],
  "Two pronouns: accusative ({ihn}, the {apple}) before dative (ihm, him). Other dative pronouns slot in the same way: Sie gibt {ihn} uns (to us), mir (to me).",
  "Two pronouns: accusative first.",
  {"wrong": "Sie gibt ihm {ihn}.", "why": "With two pronouns, the accusative comes first."})
s("F7", "ferriss", "Ferriss #7", "Is the {apple} red?", "Ist {der} {Apfel} rot?",
  "Ist:is:v:LK {der}:the:N:MF {Apfel}:{apple}:N:MF rot:red:-:MF",
  ["yes-no-question"],
  "A yes/no question starts with the verb. No 'do' needed.",
  "Start with the verb.")
s("F8", "ferriss", "Ferriss #8", "The {apples} are red.", "Die {Äpfel} sind rot.",
  "Die:the:N:VF {Äpfel}:{apples}:N:VF sind:are:v:LK rot:red:-:MF",
  ["plural", "predicate-adjective"],
  "{Apfel} → {Äpfel}: {plural-rule}. Every plural takes die. rot still has no ending after sind. Possessives take -e in the plural: meine {Äpfel}.",
  "Plural: {plural-rule}.")
s("F9", "ferriss", "Ferriss #9", "I must give it to him.", "Ich muss {ihn} ihm geben.",
  "Ich:I:N:VF muss:must:v:LK {ihn}:it:A:MF ihm:him:D:MF geben:give:v:RK",
  ["modal-verbs", "satzklammer", "pronoun-order"],
  "muss sits in position 2; geben goes to the very end. The two pronouns sit in between, accusative first.",
  "Modal second, infinitive last.",
  {"wrong": "Ich muss geben {ihn} ihm.", "why": "The infinitive goes to the end of the sentence."})
s("F10", "ferriss", "Ferriss #10", "I want to give it to her.", "Ich will {ihn} ihr geben.",
  "Ich:I:N:VF will:want:v:LK {ihn}:it:A:MF ihr:her:D:MF geben:give:v:RK",
  ["modal-verbs", "pronoun-order", "personal-pronouns"],
  "ich will means 'I want'. Modals take a bare infinitive: no zu for English 'to'. ihr is 'to her'. With sie, the verb tells you who: sie will (she wants), sie wollen (they want).",
  "wollen, not werden. No zu.",
  {"wrong": "Ich will zu {ihn} ihr geben.", "why": "Modal verbs take the infinitive without zu."})
s("F11", "ferriss", "Ferriss #11", "I'm going to know tomorrow.", "Ich werde es morgen wissen.",
  "Ich:I:N:VF werde:will:v:LK es:it:A:MF morgen:tomorrow:-:MF wissen:know:v:RK",
  ["future-werden"],
  "Future: werden in position 2, infinitive at the end. es is 'it' in the sense of 'the answer', not a thing, so it's neuter.",
  "The future uses werden.",
  {"wrong": "Ich will es morgen wissen.", "why": "ich will means 'I want'. The future uses werden."})
s("F12", "ferriss", "Ferriss #12", "I can't eat the {apple}.", "Ich kann {den} {Apfel} nicht essen.",
  "Ich:I:N:VF kann:can:v:LK {den}:the:A:MF {Apfel}:{apple}:A:MF nicht:not:-:MF essen:eat:v:RK",
  ["modal-verbs", "negation-nicht"],
  "kann in position 2, essen at the end, nicht directly before essen.",
  "nicht goes right before the infinitive.",
  {"wrong": "Ich kann nicht {den} {Apfel} essen.", "why": "Not wrong, but it means 'not the {apple} (something else)'. For plain negation, nicht goes before essen."})
s("F13", "ferriss", "Ferriss #13", "I have eaten the {apple}.", "Ich habe {den} {Apfel} gegessen.",
  "Ich:I:N:VF habe:have:v:LK {den}:the:A:MF {Apfel}:{apple}:A:MF gegessen:eaten:v:RK",
  ["perfekt", "satzklammer"],
  "Perfekt: haben in position 2, participle gegessen at the end. This is also how German says 'I ate the {apple}' in conversation.",
  "haben second, participle last.",
  {"wrong": "Ich habe gegessen {den} {Apfel}.", "why": "The participle goes to the end."})

# --------------------------------------------------------------------------
# The 41 Golden Sentences, keeping only those that add something beyond
# Ferriss's originals and each other. Dropped:
#   identical to Ferriss: #2 #3 #4 #12
#   same frame, one word swapped: #6 (F5) #7 (F6) #8 (F4) #9 (#11) #10 (F10)
#     #14 (F8) #18 (#15 + F4) #23 (#24) #26 (#21 + #15) #30 #32 (#29)
#     #33 (#31) #34 (#27) #40 (#35)
# Their small points (uns, sie/they, einige, ein paar …) live on in the notes.
# --------------------------------------------------------------------------
s("G1", "golden", "Golden 41 #1", "This is {an} {apple}.", "Das ist {ein} {Apfel}.",
  "Das:this:N:VF ist:is:v:LK {ein}:{an}:N:MF {Apfel}:{apple}:N:MF",
  ["das-demonstrative", "gender-articles"],
  "{Apfel} is {masculine} ({der}), so the indefinite article in the nominative is {ein}. Das here means 'this' and doesn't change with gender.",
  "'this is' is always das ist.")
s("G5", "golden", "Golden 41 #5", "I give John his {apple}.", "Ich gebe John {seinen} {Apfel}.",
  "Ich:I:N:VF gebe:give:v:LK John:John:D:MF {seinen}:his:A:MF {Apfel}:{apple}:A:MF",
  ["possessive-endings", "dative-accusative"],
  "The {apple} is the accusative object, so sein {sein-ending}.",
  "sein takes the same ending as ein would.")
s("G11", "golden", "Golden 41 #11", "But I do not want the {apple} either.", "Aber ich will {den} {Apfel} auch nicht.",
  "Aber:but:-:KF ich:I:N:VF will:want:v:LK {den}:the:A:MF {Apfel}:{apple}:A:MF auch:also:-:MF nicht:not:-:MF",
  ["conjunction-position-zero", "negation-nicht"],
  "aber doesn't take a slot, so the order after it is normal V2. To negate the whole statement, nicht goes after the definite object (Sie will {den} {Apfel} nicht); auch nicht = 'not either'.",
  "aber doesn't count as position 1.")
s("G13", "golden", "Golden 41 #13", "It's not mine.", "{Er} ist nicht {meiner}.",
  "{Er}:it:N:VF ist:is:v:LK nicht:not:-:MF {meiner}:mine:N:MF",
  ["pronoun-gender", "possessive-endings"],
  "'It' is {er} because it refers to {der} {Apfel}. The standalone possessive shows the gender too: {meiner}.",
  "'it' is still {der} {Apfel}.",
  {"wrong": "{Er} ist nicht mein.", "why": "Standing alone, the possessive needs a gender ending: {meiner}."})
s("G15", "golden", "Golden 41 #15", "I will not take the red {apple}.", "Ich werde {den} {roten} {Apfel} nicht nehmen.",
  "Ich:I:N:VF werde:will:v:LK {den}:the:A:MF {roten}:red:A:MF {Apfel}:{apple}:A:MF nicht:not:-:MF nehmen:take:v:RK",
  ["future-werden", "adjective-endings", "negation-nicht"],
  "werden + infinitive for the future. After {den}, the adjective takes the weak ending {weak}: {den} {roten} {Apfel}. Add a receiver and it goes before the {apple}: Ich werde dir {den} {roten} {Apfel} geben.",
  "Adjective after {den} ends in {weak}.")
s("G16", "golden", "Golden 41 #16", "Do you want {an} {apple}?", "Möchtest du {einen} {Apfel}?",
  "Möchtest:would-like:v:LK du:you:N:MF {einen}:{an}:A:MF {Apfel}:{apple}:A:MF",
  ["yes-no-question", "mochte"],
  "Verb first for a yes/no question. möchtest ('would you like') is the polite everyday way to offer something.",
  "Offer politely with möchte.")
s("G17", "golden", "Golden 41 #17", "Which one do you want?", "{Welchen} möchtest du?",
  "{Welchen}:which-one:A:VF möchtest:would-like:v:LK du:you:N:MF",
  ["w-question"],
  "welch- declines like der. It stands for a {masculine} accusative ({den} {Apfel}), so it's {welchen}.",
  "welch- ends like {den}.")
s("G19", "golden", "Golden 41 #19", "It was John's {apple}.", "Es war Johns {Apfel}.",
  "Es:it:N:VF war:was:v:LK Johns:John's:G:MF {Apfel}:{apple}:N:MF",
  ["praeteritum", "genitive-s"],
  "war is the simple past of sein. Spoken German uses war, not ist gewesen, for everyday 'was'.",
  "Simple past of sein.")
s("G20", "golden", "Golden 41 #20", "But he said he doesn't want it anymore.", "Aber er hat gesagt, dass er {ihn} nicht mehr will.",
  "Aber:but:-:KF er:he:N:VF hat:has:v:LK gesagt,:said:v:RK dass:that:-:NF er:he:N:NF {ihn}:it:A:NF nicht:not:-:NF mehr:anymore:-:NF will:wants:v:NF",
  ["subordinate-verb-final", "perfekt"],
  "The main clause is Perfekt (hat … gesagt). dass sends will to the end of its clause.",
  "dass sends the verb to the end.",
  {"wrong": "…, dass er will {ihn} nicht mehr.", "why": "After dass the conjugated verb goes last."})
s("G21", "golden", "Golden 41 #21", "So now it is yours.", "Jetzt gehört {er} also dir.",
  "Jetzt:now:-:VF gehört:belongs:v:LK {er}:it:N:MF also:so:-:MF dir:to-you:D:MF",
  ["verb-second", "dative-verbs"],
  "jetzt takes position 1, so the verb comes next and the subject {er} follows it. gehören takes a dative: 'belongs to you'.",
  "Start with jetzt; the verb still comes second.",
  {"wrong": "Jetzt {er} gehört also dir.", "why": "The verb must be second: Jetzt gehört {er}."})
s("G22", "golden", "Golden 41 #22", "You should eat it.", "Du solltest {ihn} essen.",
  "Du:you:N:VF solltest:should:v:LK {ihn}:it:A:MF essen:eat:v:RK",
  ["konjunktiv-2", "modal-verbs"],
  "solltest (subjunctive of sollen) gives advice: 'you should'. du sollst is closer to 'you're supposed to'.",
  "Advice uses sollte.")
s("G24", "golden", "Golden 41 #24", "Why didn't you eat it?", "Warum hast du {ihn} nicht gegessen?",
  "Warum:why:-:VF hast:have:v:LK du:you:N:MF {ihn}:it:A:MF nicht:not:-:MF gegessen:eaten:v:RK",
  ["w-question", "perfekt", "negation-nicht"],
  "warum first, hast second, gegessen last. nicht comes right before the participle. The yes/no version just starts with the verb: Hast du {den} {Apfel} gegessen?",
  "Question word, then hast.")
s("G25", "golden", "Golden 41 #25", "If you ate it, you would be happy.", "Wenn du {ihn} essen würdest, wärst du glücklich.",
  "Wenn:if:-:VF du:you:N:VF {ihn}:it:A:VF essen:eat:v:VF würdest,:would:v:VF wärst:would-be:v:LK du:you:N:MF glücklich:happy:-:MF",
  ["konjunktiv-2", "subordinate-verb-final", "verb-second"],
  "The wenn-clause puts würdest last. The whole clause fills position 1, so the main clause starts with its verb: wärst du.",
  "After the wenn-clause, the verb comes next.")
s("G27", "golden", "Golden 41 #27", "They will eat all of the {apples}.", "Sie werden alle {Äpfel} essen.",
  "Sie:they:N:VF werden:will:v:LK alle:all:A:MF {Äpfel}:{apples}:A:MF essen:eat:v:RK",
  ["future-werden", "plural"],
  "alle goes straight before the noun. No word for 'of'.",
  "No 'of' after alle.")
s("G28", "golden", "Golden 41 #28", "And there are a lot of {apples} to eat.", "Und es gibt viele {Äpfel} zu essen.",
  "Und:and:-:KF es:it:N:VF gibt:gives:v:LK viele:many:A:MF {Äpfel}:{apples}:A:MF zu:to:-:RK essen:eat:v:RK",
  ["es-gibt", "zu-infinitive"],
  "'There are' is es gibt, even for plurals. The object is accusative. 'to eat' is zu essen.",
  "'there are' is es gibt.")
s("G29", "golden", "Golden 41 #29", "Most of them are red.", "Die meisten von ihnen sind rot.",
  "Die:the:N:VF meisten:most:N:VF von:of:-:VF ihnen:them:D:VF sind:are:v:LK rot:red:-:MF",
  ["comparison", "dative-prepositions"],
  "die meisten = 'most'. von takes the dative: ihnen. Swap in other amounts: einige von ihnen (some), ein paar von ihnen (a few; ein Paar with a capital P is 'a pair').",
  "von takes the dative.")
s("G31", "golden", "Golden 41 #31", "And none of the {apples} are blue.", "Und {keiner} der {Äpfel} ist blau.",
  "Und:and:-:KF {keiner}:none:N:VF der:of-the:G:VF {Äpfel}:{apples}:G:VF ist:is:v:LK blau:blue:-:MF",
  ["kein", "genitive"],
  "der {Äpfel} is genitive plural ('of the {apples}'). {keiner} is singular, so the verb is ist. 'One of the {apples}' works the same way: {einer} der {Äpfel}.",
  "{keiner} is singular.")
s("G35", "golden", "Golden 41 #35", "These are beautiful, big, red {apples}.", "Das sind schöne, große, rote {Äpfel}.",
  "Das:these:N:VF sind:are:v:LK schöne,:beautiful:N:MF große,:big:N:MF rote:red:N:MF {Äpfel}:{apples}:N:MF",
  ["adjective-endings", "das-demonstrative"],
  "No article before a plural noun, so every adjective takes the strong ending -e (also: Kleine {Äpfel} sind auch gut). Das sind = 'these are'.",
  "No article, so each adjective ends in -e.")
s("G36", "golden", "Golden 41 #36", "You can have as many as you want.", "Du kannst so viele haben, wie du willst.",
  "Du:you:N:VF kannst:can:v:LK so:as:-:MF viele:many:A:MF haben,:have:v:RK wie:as:-:NF du:you:N:NF willst:want:v:NF",
  ["modal-verbs", "comparison", "subordinate-verb-final"],
  "so viele … wie = 'as many as'. The wie-clause sends willst to the end.",
  "'as many as' is so viele wie.")
s("G37", "golden", "Golden 41 #37", "Because I have enough for everyone.", "Weil ich genug für alle habe.",
  "Weil:because:-:LK ich:I:N:MF genug:enough:-:MF für:for:-:MF alle:everyone:A:MF habe:have:v:RK",
  ["subordinate-verb-final", "accusative-prepositions"],
  "weil sends habe to the end. für takes the accusative. On its own like this, it's a spoken answer to 'Warum?'.",
  "weil sends the verb to the end.",
  {"wrong": "Weil ich habe genug für alle.", "why": "Common in casual speech, but standard German puts the verb last after weil."})
s("G38", "golden", "Golden 41 #38", "Almost everyone likes {apples}.", "Fast jeder mag {Äpfel}.",
  "Fast:almost:-:VF jeder:everyone:N:VF mag:likes:v:LK {Äpfel}:{apples}:A:MF",
  ["mochte"],
  "jeder is singular, so the verb is mag (from mögen, 'to like').",
  "'everyone' is singular.")
s("G39", "golden", "Golden 41 #39", "The biggest ones are the best.", "Die größten sind die besten.",
  "Die:the:N:VF größten:biggest:N:VF sind:are:v:LK die:the:N:MF besten:best:N:MF",
  ["comparison", "adjective-endings"],
  "Superlatives used as nouns: die größten, die besten. groß adds an umlaut; gut is irregular (besser, best-).",
  "gut → besser → best-.")
s("G41", "golden", "Golden 41 #41", "But the big {apples} are better.", "Aber die großen {Äpfel} sind besser.",
  "Aber:but:-:KF die:the:N:VF großen:big:N:VF {Äpfel}:{apples}:N:VF sind:are:v:LK besser:better:-:MF",
  ["comparison", "adjective-endings"],
  "After die (plural), the adjective takes -en: die großen {Äpfel}. gut → besser.",
  "After die (plural), the adjective ends in -en.")

# --------------------------------------------------------------------------
# Gap fillers: core grammar neither list covers
# --------------------------------------------------------------------------
s("X2", "extra", "Added", "The child eats the {apple}.", "Das Kind isst {den} {Apfel}.",
  "Das:the:N:VF Kind:child:N:VF isst:eats:v:LK {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["gender-articles", "stem-vowel-change"],
  "Kind is neuter (das Kind), even though a child is a person: grammatical gender doesn't follow meaning. essen changes its vowel like geben: er isst.",
  "Kind is neuter; essen → isst.")
s("X3", "extra", "Added", "I give the child the {apple}.", "Ich gebe dem Kind {den} {Apfel}.",
  "Ich:I:N:VF gebe:give:v:LK dem:the:D:MF Kind:child:D:MF {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["dative-accusative", "gender-articles"],
  "The child receives it: neuter dative, das Kind → dem Kind. The {apple} is the thing given: {den} {Apfel}.",
  "Neuter dative is dem.",
  {"wrong": "Ich gebe der Kind {den} {Apfel}.", "why": "Kind is neuter, so the dative is dem."})
s("X4", "extra", "Added", "I don't have {an} {apple}.", "Ich habe {keinen} {Apfel}.",
  "Ich:I:N:VF habe:have:v:LK {keinen}:no:A:MF {Apfel}:{apple}:A:MF",
  ["kein"],
  "To negate a noun with ein, use kein, with the same ending: {einen} → {keinen}.",
  "Negate ein with kein.",
  {"wrong": "Ich habe nicht {einen} {Apfel}.", "why": "Use kein to negate a noun with ein: {keinen} {Apfel}."})
s("X5", "extra", "Added", "Give me the {apple}!", "Gib mir {den} {Apfel}!",
  "Gib:give:v:LK mir:me:D:MF {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["imperative"],
  "du-command: take du gibst, drop du and -st → Gib!",
  "Command form of du gibst.")
s("X6", "extra", "Added", "Would you like {an} {apple}? (formal)", "Möchten Sie {einen} {Apfel}?",
  "Möchten:would-like:v:LK Sie:you:N:MF {einen}:{an}:A:MF {Apfel}:{apple}:A:MF",
  ["formal-sie", "mochte"],
  "Formal 'you' is Sie, always capitalised, with the same verb form as 'they': möchten.",
  "Formal Sie uses the 'they' verb form.")
s("X7", "extra", "Added", "I put the {apple} on the table.", "Ich lege {den} {Apfel} auf den Tisch.",
  "Ich:I:N:VF lege:lay:v:LK {den}:the:A:MF {Apfel}:{apple}:A:MF auf:on:-:MF den:the:A:MF Tisch:table:A:MF",
  ["two-way-prepositions"],
  "Movement to a place (where to?) → auf + accusative: auf den Tisch.",
  "Movement: auf + accusative.",
  {"wrong": "Ich lege {den} {Apfel} auf dem Tisch.", "why": "legen is movement to a place, so auf takes the accusative: den Tisch."})
s("X8", "extra", "Added", "The {apple} is lying on the table.", "{Der} {Apfel} liegt auf dem Tisch.",
  "{Der}:the:N:VF {Apfel}:{apple}:N:VF liegt:lies:v:LK auf:on:-:MF dem:the:D:MF Tisch:table:D:MF",
  ["two-way-prepositions"],
  "Location (where?) → auf + dative: auf dem Tisch. Compare legen (put) and liegen (lie).",
  "Location: auf + dative.")
s("X9", "extra", "Added", "The {apple} fell off the table.", "{Der} {Apfel} ist vom Tisch gefallen.",
  "{Der}:the:N:VF {Apfel}:{apple}:N:VF ist:is:v:LK vom:from-the:D:MF Tisch:table:D:MF gefallen:fallen:v:RK",
  ["perfekt-sein", "dative-prepositions"],
  "fallen is movement, so its Perfekt uses sein. vom = von dem (von takes the dative).",
  "fallen takes sein.",
  {"wrong": "{Der} {Apfel} hat vom Tisch gefallen.", "why": "Verbs of movement form the Perfekt with sein."})
s("X10", "extra", "Added", "I'll bring {an} {apple} along tomorrow.", "Ich bringe morgen {einen} {Apfel} mit.",
  "Ich:I:N:VF bringe:bring:v:LK morgen:tomorrow:-:MF {einen}:{an}:A:MF {Apfel}:{apple}:A:MF mit:along:-:RK",
  ["separable-verbs", "future-werden"],
  "mitbringen splits: bringe in position 2, mit at the end. Present tense + morgen is the usual way to talk about the future.",
  "mitbringen splits apart.",
  {"wrong": "Ich mitbringe morgen {einen} {Apfel}.", "why": "The prefix separates and goes to the end: bringe … mit."})
s("X11", "extra", "Added", "The {apple} that I bought is red.", "{Der} {Apfel}, {den} ich gekauft habe, ist rot.",
  "{Der}:the:N:VF {Apfel},:{apple}:N:VF {den}:that:A:VF ich:I:N:VF gekauft:bought:v:VF habe,:have:v:VF ist:is:v:LK rot:red:-:MF",
  ["relative-clauses", "subordinate-verb-final"],
  "{den} is {masculine} ({der} {Apfel}) and accusative (I bought it). habe goes to the end of the relative clause.",
  "'that' takes the gender of {Apfel}: {den}.")
s("X12", "extra", "Added", "I'm looking forward to the {apple}.", "Ich freue mich auf {den} {Apfel}.",
  "Ich:I:N:VF freue:look-forward:v:LK mich:myself:A:MF auf:to:-:MF {den}:the:A:MF {Apfel}:{apple}:A:MF",
  ["reflexive-verbs"],
  "sich freuen auf + accusative = 'to look forward to'. The reflexive mich matches ich.",
  "freuen needs mich.",
  {"wrong": "Ich freue auf {den} {Apfel}.", "why": "sich freuen is reflexive: Ich freue mich."})
s("X13", "extra", "Added", "I eat {an} {apple} in the kitchen every day.", "Ich esse jeden Tag in der Küche {einen} {Apfel}.",
  "Ich:I:N:VF esse:eat:v:LK jeden:every:A:MF Tag:day:A:MF in:in:-:MF der:the:D:MF Küche:kitchen:D:MF {einen}:{an}:A:MF {Apfel}:{apple}:A:MF",
  ["word-order-tekamolo", "two-way-prepositions"],
  "Time (jeden Tag) before place (in der Küche). The new object ({einen} {Apfel}) comes late. in + dative for location.",
  "Time comes before place.")
