function Tweet(data){
	this.id = ko.observable(data.id)
	this.username = ko.observable(data.Username)
	this.body = ko.observable(data.Body)
	this.timestamp = ko.observable(data.Timestamp)
}


function TweetListViewModel(){
	var self = this;
	self.tweets_list = ko.observableArray([])
	self.username = ko.observable();
	self.body = ko.observable();

	self.addTweet = function() {
		self.save();
		self.username("");
		self.body("");
	};

	$.getJSON('/api/v2/tweets',function(tweetModels){
		var t = $.map(tweetModels.tweets_list,function (item){
			console.log(item);
			var twet = new Tweet(item);
			console.log(twet.body());
			return twet
		});
		self.tweets_list(t);
	});

	self.save = function() {
		console.log("saveing");
		return $.ajax({
			url:'/api/v2/tweets',
			data: JSON.stringify({
				'username': self.username(),
				'body': self.body()
			}),
			contentType:'application/json',
			type:'POST',
			success: function(data){
				alert("success");
				console.log("success");
				self.tweets_list.push(new Tweet({username:data.username,body:data.body}));
				return;
			},
			error: function(msg){
				console.log(msg);
				return console.log("failed ");
			}
		});
	};
}

ko.applyBindings(new TweetListViewModel());
