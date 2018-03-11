function User(data) {
	this.id = ko.observable(data.id)
	this.name = ko.observable(data.name)
	this.username = ko.observable(data.username)
	this.email = ko.observable(data.email)
	this.password = ko.observable(data.password) 
}

function UserListViewModel() {
	var self = this;
	self.user_list = ko.observableArray([]);
	self.name = ko.observable();
	self.username = ko.observable();
	self.email = ko.observable();
	self.password = ko.observable();

	self.addUser = function(){
		self.save();
		self.name("");
		self.username("");
		self.email("");
		self.password("");
	};
	self.save = function (){
		console.log("gonna ajax it away"+self.name())
		return $.ajax({
			url: '/api/v1/users',
			contentType: 'application/json',
			type: 'POST',
			data : JSON.stringify({
				'name':self.name(),
				'username':self.username(),
				'email':self.email(),
				'password':self.password(),
			}),
			success: function(data){
				alert('success');
				console.log("pushing to users arrayy");
				self.user_list.push(new User({name: data.name,username: data.username,email:data.email,password:data.password}));
				return;
			},
			error: function(){
				return console.log("failed: ");
			}
		});
	};
}

ko.applyBindings(new UserListViewModel());