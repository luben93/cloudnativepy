import Tweettemplate from './templatetweet';

export default class TweetList extends React.Component {
    render(){
        //console.log(this.props.tweets)
        let tweetlist = this.props.tweets.map(tweet => <Tweettemplate key=
            {tweet.created_at} {...tweet} />);
        return(
        <div>
            <ul className="collection">
            {tweetlist}
        </ul>
            </div>

        );
    }
}
