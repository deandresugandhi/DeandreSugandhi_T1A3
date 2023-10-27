# T1A2 Porfolio Assignment

### Student: Deandre Sugandhi

[Github Repository](https://github.com/deandresugandhi/DeandreSugandhi_T1A3)<br>
[Source Control Repository](https://github.com/deandresugandhi/DeandreSugandhi_T1A3/commits/main)

## Table of Contents
- [Style Guide](#style-guide)
- [Features & Functionalities](#features--functionalities)
- [Implementation Plan](#implementation-plan)
- [Help](#help)
- [More Screenshots](#more-screenshots)
- [References](#references)

## Style Guide

This application follows the code conventions suggested in the [PEP 8](https://peps.python.org/pep-0008/) style guide for Python code (van Rossum, et al., 2023). [Pylint](https://pypi.org/project/pylint/) and its [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) is used to help maintain consistent adherence to PEP 8. However, there are a few instances where PEP 8 suggestions are intentionally not being applied to the code. While most of the code is limited to 79 characters per line, as suggested by van Rossum, et al., (2023) (PEP 8), some lines of code are longer than this, as based on personal judgement, they would not be as readable or function as intended if separated into multiple lines.

## Features & Functionalities

__Terminal Connect Four__ is a terminal application for playing the traditional __Connect Four__ game, with several added functionalities.

### Connect Four Match

The feature generates a __Connect Four__ board and game pieces for a PvP (Player vs Player) match between 2 players. The match follows the traditional rule of __Connect Four__, using the standard-size game board (7 columns and 6 rows) and winning conditions (4 pieces stacked horizontally, vertically, or diagonally). Players take turns placing their pieces on the board by inputting a column number to drop their pieces in until a winning or game draw condition is met.

The players are also able to input two additional commands in addition to a column number for dropping pieces. __"Clear"__ simulates the slider underneath a traditional __Connect Four__ board, which clears the board of all its pieces effectively resetting the game state. __"Surrender"__ allows a player to forfeit a match and grant automatic victory to the other player. Game records are then recorded into the user accounts the players' are logged into, unless guest accounts are used (see below).

### User Account System

The feature allows a user to create their own account to store personal game data such as total games played, wins, losses, win ratio, piece color, piece type, etc. User data is stored in a JSON file named __"users.json"__ located in the root directory, in the form of a list, where each element is a dictionary representing a user account storing each unique user's information.

At the start of the game, before being able to access the game's main features, both players are prompted to setup their accounts. They can either login to their existing personal accounts, create new personal accounts, or use guest accounts which do not have full access to the functionalities of the game such as piece customization, game statistics, etc. Creating personal accounts requires users to input a unique username (with a specific format) and a four-digit PIN for registration. Username / PIN will be refused if either one is in an invalid format or the username is already associated with another account. The program also stores the login status of each user account, meaning that a player cannot attempt to login to an account that is already currently logged in.

_Notes: For now, account information including username and PIN are not encrypted when stored into the JSON file. This means that anyone having access to the JSON file can easily read all account information. This warning is displayed in-game when a user attempts to create a personal account._

### High Score System

The __high-score system__ is a feature that gathers game records from the JSON file and sorts them in descending order based on a keyword inputted by the player accessing it. Players can then view the top 5 user accounts with most games played, most wins, or highest win ratio. The top users' username, games played, wins, losses, and win ratio details are shown. Guest accounts can access this feature but are not included in it as their game histories are not recorded into the JSON file.

### Customizable Piece

Players can choose to customize how their game pieces are displayed on the game board during matches. This includes the piece type and piece color. The piece type is any single alphanumeric character chosen by the player that will be used to represent their game piece on the board, while the piece color defines the text color of the alphanumeric character. Players on a match are allowed to have the same piece color or piece type, but not both, to prevent confusion; if such a case is detected, the players are prompted to make changes to their piece properties. Players using guest accounts cannot access the piece customization feature, using the default guest account properties of __white__ __"O"__ piece for player 1 and __white__ __"X"__ piece for player 2.

### Player Lounge

The game implements a class of objects called __GameHub__, which represents lobbies or hubs with a selection of features that a user can enter and access. Each have unique ASCII art visual representations resembling a room or corridor. The __Player Lounge__ is one such hub, with accessible features including piece customization, high-score board, and user information kiosk.

#### Piece Customization

This is where players can access the __piece customization__ feature available for personal accounts only. Players are shown a preview of how their piece will look like before confirming their decision.

#### High-Score Board

This is where players can access the __high-score system__ feature. Players input a keyword for the sorting process, after which top 5 users information will be displayed in the form of an ASCII art board.

#### User Information Kiosk

The __user information kiosk__ is a feature that allows players to input any username and see their game statistics if there is an account associated with it. Information displayed include games played, wins, losses, and win ratio.

### Main Lobby

The main lobby is a __GameHub__ that acts as the landing area after both players have logged into an account. This is the hub from which the players can choose to start a Connect Four match, enter the __Player Lounge__, login to a different account, or exit the game.

## Implementation Plan

To track the development of this application, I used [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) as my project management platform (Github, Inc., 2023). First, I created a separate card for each feature of the application. Then, I created a list of tasks using checkboxes for each feature. Throughout this process, what is included in each card is reorganized to make it feel more intuitive; as a result, for example, some features are combined into a single card, while some tasks that are connected or shared between multiple features get their own separate cards. In other words, for this project, each card does not necessarily represent each separate feature of the game, but rather a group of connected tasks. For instance, the __Customizable Piece__ feature and the game board from the __Connect Four Match__ feature are combined into a single card called __Game Board__, which represents the objects involved in a physical Connect Four game, namely the piece and the board. There is also a dedicated card called __Win / Draw Conditions__ despite it not being its own separate feature but a part of the __Connect Four Match__ feature, as I feel it is more helpful for me to separate the rules of the game from the game objects itself.

I used the GitHub project's default labels as well as my own custom labels to help prioritize each card, such as using a __core__ label for cards that is an integral part of the application, __enhancement__ label for cards with functionalities that enhances user experience and are thus optional depending on the time available until deadline, __core complete__ label for cards with all core tasks completed, and __fully completed__ label for cards with all tasks fully completed.

The __Roadmap__ and __Table__ view is helpful to add due dates and keep track of schedule, though in the end they are not really followed as my initial estimates of how long each card would take to complete turned out to be quite off, though it does help in deciding how to prioritize my time for each task. New features are also added as I work on the app and got new ideas, from which I checked the __Roadmap__ and due dates for each task; if I was well ahead of schedule, I would go on to try and implement the new features.

__The link to the GitHub project can be found here: [T1A3 GitHub Project](https://github.com/users/deandresugandhi/projects/1)__

__A more detailed, chronologically ordered series of screenshots can be accessed in the [More Screenshots](#more-screenshots) section of this document.__





### Experiences
The "Experiences" page contains my educational and professional history. It is divided into three HTML sections, one for education, one for work, and one for my IT-related projects. The information is displayed through the use of two article elements with flexbox layout, namely "Date" and "Description". "Date" is written as a vertically-oriented text next to "Description" which details the education or work history.

On the bottom of the page is a clickable button which downloads my resume on click.

### About
The "About" page provides further information about me, separated into three sections, namely background, skills, and hobbies. 

The background section contains a centred text component and my picture. It describes what I do for the last couple of years, and my decision to study IT.

The skills component contains left-aligned text as well as various articles and divs to showcase my IT skills. These are placeholder contents for the purpose of this assignment.

The hobbies component contains right-aligned text describing my interests.

### Blog
The "Blog" page contains five hyperlinked components each linked to their respective blog posts. Each component consist of an image, a blog title, a sub-heading stating the post's published date and its estimated read time, and a short description of the post's content. These are placeholder contents for the purpose of this assignment. Each component changes colour on hover to indicate that it is a clickable link.

### Contacts
The contact page contains a short message from me, my contact details (phone, email, and address), and a set of icons linking to my social / professional accounts. Each icon changes colour on hover to indicate that they are clickable links.

### Blogposts
The main content of each blogpost page contains the title of the post, a sub-heading stating its published date and estimated read time, an image, and an article. All are placeholder contents for now. 

Under the main content, there is a "Recent Posts" section which contains 4 components linked to 4 of the most recent posts of the blog (excluding the post currently being opened). As there are only 5 blogposts for now, each blogpost have direct access to all the rest of the blogposts. Because these pages are not the main blog page where viewers need to be able to read the full title of the posts, the titles of the blogposts in the "Recent Posts" section are truncated with an ellipsis based on the size of its container, which alters based on screen size.

## Sitemap
![Sitemap](./docs/sitemap.png)
Black arrows indicates links based on navigation bar, red arrows indicate links based on other elements in the page.

## Screenshots
Screenshots are taken full-size.

### Mobile
#### Home
![home](./docs/screenshots/homephone.png)
#### Experiences
![experiences](./docs/screenshots/experiencesphone.png)
#### About
![about](./docs/screenshots/aboutphone.png)
#### Blog
![blog](./docs/screenshots/blogphone.png)
#### Contact
![contact](./docs/screenshots/contactphone.png)
#### Blogpost
![blogpost](./docs/screenshots/blogpostphone.png)

### Tablet
#### Home
![home](./docs/screenshots/hometablet.png)
#### Experiences
![experiences](./docs/screenshots/experiencestablet.png)
#### About
![about](./docs/screenshots/abouttablet.png)
#### Blog
![blog](./docs/screenshots/blogtablet.png)
#### Contact
![contact](./docs/screenshots/contacttablet.png)
#### Blogpost
![blogpost](./docs/screenshots/blogposttablet.png)

### Desktop (1920 x 1080)
#### Home
![home](./docs/screenshots/homedesktop.png)
#### Experiences
![experiences](./docs/screenshots/experiencesdesktop.png)
#### About
![about](./docs/screenshots/aboutdesktop.png)
#### Blog
![blog](./docs/screenshots/blogdesktop.png)
#### Contact
![contact](./docs/screenshots/contactdesktop.png)
#### Blogpost
![blogpost](./docs/screenshots/blogpostdesktop.png)

## Wireframes
### Mobile
#### Home
![home](./docs/wireframes/wireframehomephone.png)
#### Experiences
![experiences](./docs/wireframes/wireframeexperiencesphone.png)
#### About
![about](./docs/wireframes/wireframeaboutphone.png)
#### Blog
![blog](./docs/wireframes/wireframeblogphone.png)
#### Contact
![contact](./docs/wireframes/wireframecontactphone.png)
#### Blogpost
![blogpost](./docs/wireframes/wireframeblogpostphone.png)

### Tablet
#### Home
![home](./docs/wireframes/wireframehometablet.png)
#### Experiences
![experiences](./docs/wireframes/wireframeexperiencestablet.png)
#### About
![about](./docs/wireframes/wireframeabouttablet.png)
#### Blog
![blog](./docs/wireframes/wireframeblogtablet.png)
#### Contact
![contact](./docs/wireframes/wireframecontacttablet.png)
#### Blogpost
![blogpost](./docs/wireframes/wireframeblogposttablet.png)

### Desktop (1920 x 1080)
#### Home
![home](./docs/wireframes/wireframehomedesktop.png)
#### Experiences
![experiences](./docs/wireframes/wireframeexperiencesdesktop.png)
#### About
![about](./docs/wireframes/wireframeaboutdesktop.png)
#### Blog
![blog](./docs/wireframes/wireframeblogdesktop.png)
#### Contact
![contact](./docs/wireframes/wireframecontactdesktop.png)
#### Blogpost
![blogpost](./docs/wireframes/wireframeblogpostdesktop.png)

## Tech Stack
- Website: HTML, CSS, JavaScript
- Sitemap: [draw.io](https://app.diagrams.net/)
- Wireframe: [draw.io](https://app.diagrams.net/)
- Deployment: [Vercel](https://vercel.com/)
- Slide deck: [Microsoft Power Point](https://www.microsoft.com/en-au/microsoft-365/powerpoint)
- Icons: [Icon Finder](https://www.iconfinder.com/)
- Royalty-Free Stock Images: [Unsplash](https://unsplash.com/)