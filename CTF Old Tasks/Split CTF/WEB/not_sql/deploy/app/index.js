const express = require('express');
const mongoose = require('mongoose');

const MONGO_URL = process.env.MONGO_URL || 'mongodb://mongo:27017/ctf';
const PORT = parseInt(process.env.PORT || '3000', 10);

// Ensure classic NoSQL injection behaviour for training/CTF purposes.
mongoose.set('sanitizeFilter', false);

const UserSchema = new mongoose.Schema({
  name: String,
  user: String,
  pass: String,
});

const User = mongoose.model('User', UserSchema);

async function seed() {
  const creds = [
    ['SplitCTF{NoSQLInjectionExample}', 'fareastctfadmin', 'adminpassword'],
    ['User', 'user', 'user'],
    ['Jules', 'bad', 'motherfucker'],
  ];

  // Keep DB stable across restarts.
  for (const [name, user, pass] of creds) {
    await User.updateOne(
      { user, pass },
      { $setOnInsert: { name, user, pass } },
      { upsert: true }
    );
  }
}

async function main() {
  await mongoose.connect(MONGO_URL);
  await seed();

  const app = express();

  app.set('views', __dirname);
  app.set('view engine', 'pug');

  // IMPORTANT: extended=true keeps nested params like user[$gt]
  app.use(express.urlencoded({ extended: true }));

  app.get('/', (req, res) => res.render('index', {}));

  app.post('/', (req, res) => {
    User.findOne({ user: req.body.user, pass: req.body.pass })
      .then((user) => {
        if (!user) return res.render('index', { message: 'Sorry!' });
        return res.render('index', { message: 'Welcome back ' + user.name + '!!!' });
      })
      .catch((err) => res.render('index', { message: err.message }));
  });

  app.listen(PORT, () => console.log('listening on port %d', PORT));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
