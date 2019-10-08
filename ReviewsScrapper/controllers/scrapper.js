const axios = require('axios');
const cheerio = require('cheerio');

exports.scrapper = async function(req, res, next) {
  let reviews = [];
  let promises = [];
  let page = 1;
  console.log(req.query);
  let url = req.query.url;

  while (page < 5) {
    if (page !== 1) {
      url = url + '&page=' + page;
    }

    await axios
      .get(url)
      .then(async response => {
        if (response.status === 200) {
          const html = response.data;
          const $ = cheerio.load(html);

          await $('.gr_more_link').each(async function() {
            let review_url = $(this).attr('href');
            console.log(review_url);

            promises.push(axios.get(review_url));
          });
        }
      })
      .catch(err => {
        next(err);
      });

    page += 1;
  }

  await axios
    .all(promises)
    .then(results => {
      results.forEach(response => {
        let temp = cheerio.load(response.data);

        let reviewer = temp('.reviewer a.userReview').text();
        let text = temp('.reviewText').text();
        let date = temp('div.dtreviewed span.value-title').attr('title');
        let rating = temp('div.rating span.value-title').attr('title');

        let review = { reviewer, text, date, rating };
        reviews.push(review);
      });
    })
    .catch(err => {
      next(err);
    });

  return res.status(200).json(reviews);
};
