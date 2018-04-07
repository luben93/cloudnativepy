import Tweet from "./components/Tweet";
import TweetList from "./components/TweetList"
import cookie from 'react-cookie';


class Main extends React.Component{
    constructor(props){
    super(props);
  //  this.state = { userId: cookie.load('session') };
    this.state={tweets:[{'id':1,'tweetedby':'guest','body':'butts #butt','timestamp':Date.now()}]}
}

    render(){
 //       console.log(this.state.tweets)
        return (
        <div>
            <Tweet sendTweet={this.addTweet.bind(this)} />
            <TweetList tweets={ this.state.tweets }/>
            </div>

        );

    }



    addTweet(tweet){
        var self = this;
        $.ajax({
            url: '/api/v2/tweets',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({
                'username': "Agnsur",
                'body': tweet,

            }),
            success: function(data) {
            let newTweetList = self.state.tweets;
            newTweetList.unshift({ tweetedby: "Saussiona55",body: tweet, timestamp: Date.now });
            self.setState({tweets: newTweetList})
                return console.log("success");

            },
            error: function(data) {
                console.log(data)
                return console.log("Failed");

            }

        });

    }

    componentDidMount() {
        var self=this;
        $.ajax({url: `/api/v2/tweets`,
            success: function(data) {
                var t = data['tweets_list'];
               // console.log(t);
               // var t1 = JSON.parse(t[0] );
               // console.log(t1);
                self.setState({tweets: t});
            //   alert(self.state.tweets);
               // return console.log("success");

            },
            error: function() {
                return console.log("Failed");

            }
        });
    }
}
let documentReady =() =>{
    ReactDOM.render(
    <Main />,
        document.getElementById('react')

    );

};


$(documentReady);
