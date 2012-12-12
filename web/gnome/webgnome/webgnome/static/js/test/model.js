define([
    'models',
    'test/fixtures/timesteps',
], function(models, data) {

    module('Model');

    var origAjax = $.ajax;
    var testUrl = "http://localhost/test";

    function makeModel(timeSteps, expectedTimeSteps) {
        return new models.Model(timeSteps || [], {
            url: testUrl,
            expectedTimeSteps: expectedTimeSteps || []
        });
    }

    // Tests

    test('hasData should return false if expectedTimeSteps is empty', function() {
        var model = makeModel();
        ok(model.hasData() === false);
    });

     test('hasData should be true if expectedTimeSteps has items', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.hasData() === true);
    });

    test('hasCachedTimeStep should be true if item is cached', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.hasCachedTimeStep(2) === true);
    });

    test('hasCachedTimeStep should be false if item is not cached', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.hasCachedTimeStep(data.timeSteps.length + 1) === false);
    });
    
    test('serverHasTimeStep should be true if the server expects to generate the time step', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.serverHasTimeStep(2) === true);
    });

    test('serverHasTimeStep should be true if the server does not expect to generate the time step', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.serverHasTimeStep(data.timeSteps.length + 1) === false);
    });   


    test('getTimestampForExpectedStep should return a timestamp if step exists', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        console.log(model.getTimestampForExpectedStep(0));
        ok(model.getTimestampForExpectedStep(0) === 'Fri, 07 Dec 2012 12:00:00 GMT');
    });

    test('getTimestampForExpectedStep should return undefined if step does not exist', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        ok(model.getTimestampForExpectedStep(10) === undefined);
    });

    test('getCurrentTimeStep should return the correct TimeStep object', function() {
        var model = makeModel(data.timeSteps, data.expectedTimeSteps);
        var timeStep = model.getCurrentTimeStep();
        ok(timeStep.get('id') === 0);
        ok(timeStep.get('timestamp') === 'Fri, 07 Dec 2012 12:00:00 GMT');

        model.currentTimeStep = 1;
        timeStep = model.getCurrentTimeStep();
        ok(timeStep.get('id') === 1);
        ok(timeStep.get('timestamp') === "Fri, 07 Dec 2012 12:15:00 GMT");
    });
});