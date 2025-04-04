use bb8::{ManageConnection, Pool};
use std::convert::Infallible;
use std::fs::File;
use std::io::Write;
use std::time::Instant;

pub struct IntManager;

use std::future::ready;

impl ManageConnection for IntManager {
    type Connection = i32;
    type Error = Infallible;

    fn connect(&self) -> impl Future<Output = Result<Self::Connection, Self::Error>> + Send {
        ready(Ok(0))
    }

    fn is_valid(
        &self,
        _conn: &mut Self::Connection,
    ) -> impl Future<Output = Result<(), Self::Error>> + Send {
        ready(Ok(()))
    }

    fn has_broken(&self, _conn: &mut Self::Connection) -> bool {
        false
    }
}

#[tokio::main]
async fn main() {
    let mut file = File::create("bb8-result.txt").unwrap();
    let iters = 1_000;
    let worker_iters = 10;
    for pool_size in [4, 8, 16] {
        for workers in [4, 16, 64, 256] {
            let pool = Pool::builder()
                .max_size(pool_size)
                .build(IntManager)
                .await
                .unwrap();

            // reserve resources.
            let mut v = Vec::with_capacity(pool_size as usize);
            for _ in 0..pool_size {
                v.push(pool.get().await.unwrap());
            }
            drop(v);

            let mut elapsed = Vec::with_capacity(iters);
            for _ in 0..iters {
                let start = Instant::now();
                let handles = (0..workers)
                    .map(|_| {
                        let pool = pool.clone();
                        tokio::spawn(async move {
                            for _ in 0..worker_iters {
                                let mut int = pool.get().await.unwrap();
                                *int += 1;
                            }
                        })
                    })
                    .collect::<Vec<_>>();
                for handle in handles {
                    handle.await.unwrap();
                }
                elapsed.push(start.elapsed());
            }
            elapsed.sort();
            let median = elapsed[iters / 2];
            let q1 = elapsed[iters / 4];
            let q3 = elapsed[iters * 3 / 4];
            println!(
                "bb8 (pool={}, worker={}): {:?} (Q1={:?}, Q3={:?})",
                pool_size, workers, median, q1, q3,
            );
            writeln!(
                file,
                "bb8,{},{},{},{},{}",
                pool_size,
                workers,
                q1.as_nanos(),
                median.as_nanos(),
                q3.as_nanos()
            )
            .unwrap();
        }
    }
}
