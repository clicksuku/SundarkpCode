// Reference - https://medium.com/@rahulguptalive/create-crud-apis-in-nodejs-express-and-mysql-abda4dfc2d6

const express = require('express')
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express()
const port = 7000

const outcomeRouter = require('./routes/outcomeRoute');
const programRouter = require('./routes/programRoute');
const peopleRouter = require('./routes/peopleRouter');
const changeRequestRouter = require('./routes/changeRequestRoute');
const externalOrgMasterRouter = require('./routes/externalOrgMasterRoute');
const externalTeamsMasterRouteRouter = require('./routes/externalTeamsMasterRoute');
const paymentDomainsRouter = require('./routes/paymentsDomainsRoute');
const outcomePeopleRouter = require('./routes/outcomePeopleRoute');
const outcomeProgramRouter = require('./routes/outcomeProgramRoute');
const estimateRouter = require('./routes/estimateRoute');
const peopleQuarterAvailabilityRouter = require('./routes/peopleQuarterAvailabilityRouter');

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())
app.use(cors());

app.listen(port, () => console.log(`Example app listening on port ${port}!`))

//Root
app.get('/', (req, res) => res.send('Root World!'))

//API
app.get('/api', (req, res) => res.send('Data Services World!'))


//Outcomes
app.use('/api/outcomes',outcomeRouter);

//Programs
app.use('/api/programs',programRouter);

//People
app.use('/api/people',peopleRouter);

//People
app.use('/api/externalorgs',externalOrgMasterRouter);

//Change Requests
app.use('/api/changerequests',changeRequestRouter);

//External Teams
app.use('/api/externalteams',externalTeamsMasterRouteRouter);

//Payments Domains
app.use('/api/paymentsdomains',paymentDomainsRouter);

//OutcomePeopleMapping
app.use('/api/outcomepeoplemapping',outcomePeopleRouter);

//OutcomeProgramMapping
app.use('/api/outcomeprogrammapping',outcomeProgramRouter);

//Estimates
app.use('/api/estimates',estimateRouter);

//PeopleQuarterAvailability
app.use('/api/peopleQuarterAvailability',peopleQuarterAvailabilityRouter);