class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.followers = []
        self.following = []

class Post:
    def __init__(self, text, image_url, user):
        self.text = text
        self.image_url = image_url
        self.likes = 0
        self.user = user
        self.tags = []
        self.comments = []

class Comment:
    def __init__(self, text, user):
        self.text = text
        self.user = user

class InstagramSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password, email):
        user = User(username, password, email)
        if username in self.users:
            return -1  # Username already exists
        self.users[username] = user
        return 0

    def login(self, username, password):
        if username not in self.users or self.users[username].password != password:
            return -1  # Incorrect username or password
        return self.users[username]

    def post(self, user, text, image_url):
        post = Post(text, image_url, user)
        self.users[user.username].posts.append(post)
        return post

    def like(self, post_id, user):
        post = self.find_post(post_id, user)
        if post:
            post.likes += 1
            return 0
        return -1

    def comment(self, post_id, user, text):
        post = self.find_post(post_id, user)
        if post:
            post.comments.append(Comment(text, user))
            return 0
        return -1

    def find_post(self, post_id, user):
        for u in self.users.values():
            for post in u.posts:
                if post.id == post_id:
                    if post.user == user or user.username == 'admin':
                        return post
        return None

    def follow(self, user1, user2):
        user1_following = self.users[user1.username].following
        if user2 not in user1_following:
            user1_following.append(user2)
            user2_followers = self.users[user2.username].followers
            if user1 not in user2_followers:
                user2_followers.append(user1)
            return 0
        return -1

    def unfollow(self, user1, user2):
        user1_following = self.users[user1.username].following
        if user2 in user1_following:
            user1_following.remove(user2)
            user2_followers = self.users[user2.username].followers
            if user1 in user2_followers:
                user2_followers.remove(user1)
            return 0
        return -1

    def get_profile(self, username):
        if username in self.users:
            return self.users[username]
        return None

    def get_feed(self, user):
        feed = []
        user_following = self.users[user.username].following
        for user in user_following:
            for post in self.users[user.username].posts:
                feed.append((post, self.users[user.username]))
        return feed

def main():
    ig = InstagramSystem()
    while True:
        print('1. Register')
        print('2. Login')
        print('3. Post')
        print('4. Like')
        print('5. Comment')
        print('6. Follow')
        print('7. Unfollow')
        print('8. Get profile')
        print('9. Get feed')
        print('0. Quit')
        choice = input('Choose an option: ')
        if choice == '1':
            username = input('Enter username: ')
            password = input('Enter password: ')
            email = input('Enter email: ')
            result = ig.register_user(username, password, email)
            if result == 0:
                print('User registered successfully')
            elif result == -1:
                print('Username already exists')
        elif choice == '2':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user = ig.login(username, password)
            if user:
                print('Login successful')
            else:
                print('Incorrect username or password')
        elif choice == '3':
            username = input('Enter username: ')
            text = input('Enter text: ')
            image_url = input('Enter image URL: ')
            post = ig.post(username, text, image_url)
            if post:
                print('Post created successfully')
        elif choice == '4':
            post_id = int(input('Enter post ID: '))
            username = input('Enter username: ')
            result = ig.like(post_id, username)
            if result == 0:
                print('Post liked successfully')
            else:
                print('Post not found')
        elif choice == '5':
            post_id = int(input('Enter post ID: '))
            username = input('Enter username: ')
            text = input('Enter comment: ')
            result = ig.comment(post_id, username, text)
            if result == 0:
                print('Comment added successfully')
            else:
                print('Post not found')
        elif choice == '6':
            user1_username = input('Enter username of user to follow: ')
            user2_username = input('Enter username of user to follow you: ')
            result = ig.follow(user1_username, user2_username)
            if result == 0:
                print('Followed successfully')
            else:
                print('Already following')
        elif choice == '7':
            user1_username = input('Enter username of user to unfollow: ')
            user2_username = input('Enter username of user you want to unfollow: ')
            result = ig.unfollow(user1_username, user2_username)
            if result == 0:
                print('Unfollowed successfully')
            else:
                print('Not following')
        elif choice == '8':
            username = input('Enter username: ')
            user = ig.get_profile(username)
            if user:
                print('Username: ', user.username)
                print('Email: ', user.email)
                print('Followers: ', len(user.followers))
                print('Following: ', len(user.following))
        elif choice == '9':
            username = input('Enter username: ')
            user = ig.get_profile(username)
            if user:
                feed = ig.get_feed(user)
                for post, poster in feed:
                    print('Text: ', post.text)
                    print('Image URL: ', post.image_url)
                    print('Likes: ', post.likes)
                    print('Comments: ')
                    for comment in post.comments:
                        print('Comment: ', comment.text)
                    print('\n')
        elif choice == '0':
            break
        else:
            print('Invalid option')

if __name__ == '__main__':
    main()

This executable program implements the Instagram system as per the given requirements.