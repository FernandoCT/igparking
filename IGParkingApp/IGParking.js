ParkingStatus = new Mongo.Collection("parkingStatus");

PARKING_CAPACITY = 4;

// Client

if (Meteor.isClient) {
  
  function freeSpotsCount() {
    var freeSpots = 0
    var status = ParkingStatus.findOne();
    if (status) {
      freeSpots = status.freeSpotsCount;
    }
    return freeSpots;
  };

  Template.parking.helpers({
    freeSpotsCount: function () {
      return freeSpotsCount();
    },
    hasFreeSpots: function () {
      return freeSpotsCount() > 0;
    }
  });

  Template.parking.events({
    'click #refresh': function () {
      Router.go('/');
    }
  });
}

// Server

if (Meteor.isServer) {
  Meteor.startup(function () {
    // initialize parking lot status
    var status = ParkingStatus.findOne();
    if (!status) {
      ParkingStatus.insert({freeSpotsCount: PARKING_CAPACITY});
    };
  });
}

// Client routes

Router.configure({
  layoutTemplate: 'mainLayout'
});

Router.route('/', function () {
  this.render('parking');
});

// Rest endpoints

Router.route('/updatestatus/:freeSpots', function () {
  var freeSpots = this.params.freeSpots;
  // update the parking status
  var status = ParkingStatus.findOne();
  ParkingStatus.update({_id: status._id}, {$set: {freeSpotsCount: freeSpots}});
  // return message
  var res = this.response;
  res.end('current free spots count = ' + freeSpots);
}, {where: 'server'});
